"""Evidence files are copied only after size, extension, and digest checks."""

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import shutil

from ..domain.validation import integer

MAX_MEDIA_BYTES = 16 * 1024 * 1024
ALLOWED_TYPES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".txt": "text/plain", ".json": "application/json"}


@dataclass(frozen=True)
class Evidence:
    name: str
    media_type: str
    bytes: int
    sha256: str
    created_at: str


def _hash(path):
    digest = hashlib.sha256()
    size = 0
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(block)
            if size > MAX_MEDIA_BYTES:
                raise ValueError(f"evidence exceeds {MAX_MEDIA_BYTES} bytes")
            digest.update(block)
    return size, digest.hexdigest()


def inspect_file(path):
    path = Path(path).resolve()
    if path.is_symlink() or not path.is_file():
        raise ValueError("evidence must be a regular file")
    media_type = ALLOWED_TYPES.get(path.suffix.lower())
    if media_type is None:
        raise ValueError("unsupported evidence extension")
    size, digest = _hash(path)
    return Evidence(path.name, media_type, size, digest, datetime.now(timezone.utc).isoformat())


def ingest_file(path, destination):
    evidence = inspect_file(path)
    destination = Path(destination).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise ValueError("evidence destination already exists")
    shutil.copyfile(Path(path), destination)
    copied = inspect_file(destination)
    if copied.sha256 != evidence.sha256 or copied.bytes != evidence.bytes:
        destination.unlink(missing_ok=True)
        raise ValueError("evidence changed during copy")
    return copied
