"""Dependency-free validation of the repository's benchmark metadata contract."""

import json
from pathlib import Path
import re

from ..domain.validation import integer


def read_manifest(path):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {"id", "title", "domain", "subdomain", "mechanism", "category", "rounds", "constraints", "setup", "verify"}
    optional = {"public_checks", "tags"}
    if not isinstance(value, dict) or not required <= set(value) or set(value) - required - optional:
        raise ValueError("invalid case manifest fields")
    if not isinstance(value["id"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{2,63}", value["id"]):
        raise ValueError("invalid case id")
    for name in required - {"rounds", "constraints"}:
        if not isinstance(value[name], str) or not value[name].strip():
            raise ValueError("case text field is empty: " + name)
    if not 3 <= len(value["title"]) <= 120 or not re.match(r"^F[0-9]{2} ", value["category"]):
        raise ValueError("invalid case title or category")
    integer(value["rounds"], "rounds", 1, 10)
    for name in ("constraints", "public_checks", "tags"):
        items = value.get(name, [])
        if not isinstance(items, list) or not all(isinstance(item, str) and item.strip() for item in items) or len(set(items)) != len(items):
            raise ValueError("case list must contain unique nonempty strings: " + name)
    return value
