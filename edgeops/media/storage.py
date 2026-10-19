"""Deterministic evidence paths prevent traversal and duplicate names."""

from pathlib import Path
import re


def evidence_path(root, digest, name):
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError("digest must be lowercase SHA-256")
    original_name = name
    name = Path(name).name
    if original_name != name or name != name.strip() or name in {"", ".", ".."} or any(ord(char) < 32 for char in name):
        raise ValueError("invalid evidence name")
    return Path(root).resolve() / digest[:2] / f"{digest}-{name}"
