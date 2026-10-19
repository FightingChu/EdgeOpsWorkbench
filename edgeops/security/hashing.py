"""Streaming SHA-256 for evidence manifests and release checks."""

import hashlib
from pathlib import Path


def sha256_file(path, block_size=1024 * 1024):
    if type(block_size) is not int or not 4096 <= block_size <= 8 * 1024 * 1024:
        raise ValueError("block_size must be between 4096 and 8388608")
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(block_size), b""):
            digest.update(block)
    return digest.hexdigest()
