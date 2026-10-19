"""Copy maintained files, inject a defect, and reset only a matching marked copy."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from .catalog import ROOT
from .manifest import read_manifest
from .patches import apply_fault, load_fault


MARKER = ".edgeops-case.json"


def maintained_files(root=ROOT):
    root = Path(root).resolve()
    result = subprocess.run(["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                            check=True, capture_output=True)
    paths = sorted(set(result.stdout.decode("utf-8").split("\x00")) - {""})
    return [path for path in paths if (root / path).is_file()]


def _safe_target(target, source=ROOT):
    target = Path(target).resolve()
    source = Path(source).resolve()
    home = Path.home().resolve()
    if (target == source or target in source.parents or source in target.parents
            or target == home or target in home.parents or target == Path(target.anchor)):
        raise ValueError("target must be outside the repository and cannot be a home, drive root, or ancestor")
    return target


def setup_case(case_directory, target, *, source=ROOT):
    source = Path(source).resolve()
    target = _safe_target(target, source)
    if target.exists():
        raise ValueError("case destination must not exist")
    case_directory = Path(case_directory)
    manifest = read_manifest(case_directory / "manifest.json")
    fault = load_fault(case_directory / "fault.json")
    files = maintained_files(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    hashes = {}
    with tempfile.TemporaryDirectory(prefix=".edgeops-case-", dir=target.parent) as temporary:
        stage = Path(temporary) / "workspace"
        stage.mkdir()
        for relative in files:
            original = (source / relative).resolve()
            if source not in original.parents:
                raise ValueError("maintained file resolves outside repository")
            output = stage / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(original.read_bytes())
            hashes[relative] = hashlib.sha256(output.read_bytes()).hexdigest()
        apply_fault(stage, fault)
        marker = {"version": 1, "case_id": manifest["id"], "target": str(target), "source": str(source),
                  "source_hashes": hashes, "changed": [fault["file"]]}
        (stage / MARKER).write_text(json.dumps(marker, indent=2) + "\n", encoding="utf-8")
        stage.rename(target)
    return marker


def reset_case(target, *, source=ROOT):
    target = _safe_target(target, source)
    marker = json.loads((target / MARKER).read_text(encoding="utf-8"))
    if marker.get("version") != 1 or marker.get("target") != str(target) or marker.get("source") != str(Path(source).resolve()):
        raise ValueError("case marker does not identify this exact disposable target")
    # All recursive deletion stays within this resolved, explicitly supplied target.
    if (target / MARKER).resolve().parent != target or target.is_symlink():
        raise ValueError("case marker or workspace is a symbolic link")
    shutil.rmtree(target)
