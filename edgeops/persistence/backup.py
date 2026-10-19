"""Consistent SQLite snapshots and verified restore into a new directory."""

import hashlib
from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import tempfile

from ..domain.backup import validate_manifest
from .diagnostics import inspect_database, readonly
from .migrations import SCHEMA_VERSION
from .repositories import utc_now


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_backup(directory):
    root = Path(directory)
    manifest_path = root / "manifest.json"
    if manifest_path.stat().st_size > 16384:
        raise ValueError("backup manifest exceeds 16384 bytes")
    manifest = validate_manifest(json.loads(manifest_path.read_text(encoding="utf-8")))
    if manifest["schema_version"] > SCHEMA_VERSION:
        raise ValueError("backup schema is newer than supported")
    path = root / manifest["database"]
    if path.is_symlink() or manifest_path.is_symlink():
        raise ValueError("backup files must be regular local files")
    if path.stat().st_size != manifest["bytes"] or file_hash(path) != manifest["sha256"]:
        raise ValueError("backup size or sha256 mismatch")
    report = inspect_database(path)
    if not report["ok"] or report["schema_version"] != manifest["schema_version"]:
        raise ValueError("backup integrity or schema mismatch")
    return manifest


def create_backup(database_path, destination):
    target = Path(destination).resolve()
    if target.exists():
        raise ValueError("backup destination must not exist")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".edgeops-backup-", dir=target.parent) as temporary:
        stage = Path(temporary) / "snapshot"
        stage.mkdir()
        path = stage / "edgeops.sqlite3"
        with readonly(database_path) as source:
            with closing(sqlite3.connect(path)) as output:
                source.backup(output)
        report = inspect_database(path)
        if not report["ok"]:
            raise ValueError("source database failed integrity checks")
        manifest = {"version": 1, "schema_version": report["schema_version"], "sha256": file_hash(path),
                    "bytes": path.stat().st_size, "created_at": utc_now(), "database": "edgeops.sqlite3"}
        (stage / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        verify_backup(stage)
        os.rename(stage, target)
    return manifest


def restore_backup(directory, destination):
    target = Path(destination).resolve()
    if target.exists():
        raise ValueError("restore destination must not exist")
    target.parent.mkdir(parents=True, exist_ok=True)
    manifest = verify_backup(directory)
    with tempfile.TemporaryDirectory(prefix=".edgeops-restore-", dir=target.parent) as temporary:
        stage = Path(temporary) / "restored"
        stage.mkdir()
        path = stage / "edgeops.sqlite3"
        # Hash the actual bytes restored as well as the source, catching changes
        # between verification and copying without modifying the original backup.
        with (Path(directory) / "edgeops.sqlite3").open("rb") as source, path.open("xb") as output:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                output.write(block)
        if file_hash(path) != manifest["sha256"] or not inspect_database(path)["ok"]:
            raise ValueError("backup changed during restore")
        os.rename(stage, target)
    return str(target / "edgeops.sqlite3")
