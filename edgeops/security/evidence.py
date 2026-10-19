"""Evidence manifest validation keeps hashes and relative paths explicit."""

import re


def validate_hash_entry(entry):
    if not isinstance(entry, dict) or set(entry) != {"path", "sha256", "bytes"}:
        raise ValueError("hash entry fields must be path, sha256, bytes")
    if not isinstance(entry["path"], str) or not entry["path"] or entry["path"].startswith(("/", "\\")) or ".." in entry["path"].split("/"):
        raise ValueError("hash path must be relative")
    if not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"]):
        raise ValueError("invalid sha256")
    if type(entry["bytes"]) is not int or not 0 <= entry["bytes"] <= 2**63 - 1:
        raise ValueError("invalid byte count")
    return entry
