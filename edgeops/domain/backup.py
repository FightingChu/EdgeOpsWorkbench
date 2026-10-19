"""Portable, versioned backup manifest contract."""

import re

from .validation import integer


def validate_manifest(value):
    keys = {"version", "schema_version", "sha256", "bytes", "created_at", "database"}
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError("invalid backup manifest fields")
    if type(value["version"]) is not int or value["version"] != 1:
        raise ValueError("unsupported backup manifest version")
    integer(value["schema_version"], "schema_version", 1, 1000000)
    integer(value["bytes"], "bytes", 1, 2**63 - 1)
    if not isinstance(value["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", value["sha256"]):
        raise ValueError("invalid backup sha256")
    if value["database"] != "edgeops.sqlite3":
        raise ValueError("backup database must be edgeops.sqlite3")
    from .events import event_timestamp
    event_timestamp(value["created_at"])
    return value
