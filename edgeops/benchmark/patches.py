"""Exact-match fault injection rejects drift instead of patching an unknown site."""

import json
from pathlib import Path


def load_fault(path):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict) or set(value) != {"file", "old", "new", "checks"}:
        raise ValueError("fault fields must be file, old, new, and checks")
    relative = value["file"]
    if not isinstance(relative, str) or "\\" in relative or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError("fault file must be a relative path inside the copy")
    if not all(isinstance(value[key], str) and value[key] for key in ("old", "new")) or value["old"] == value["new"]:
        raise ValueError("fault must contain distinct nonempty old and new text")
    if not isinstance(value["checks"], list) or not value["checks"] or not all(isinstance(item, str) and (item.startswith("tests.test_") or item.startswith("public_tests.")) for item in value["checks"]):
        raise ValueError("fault needs repository unittest checks")
    return value


def apply_fault(root, fault):
    root = Path(root).resolve()
    path = (root / fault["file"]).resolve()
    if root not in path.parents or not path.is_file():
        raise ValueError("fault target is outside the disposable workspace")
    content = path.read_text(encoding="utf-8")
    if content.count(fault["old"]) != 1:
        raise ValueError("fault precondition mismatch: expected one exact match")
    path.write_text(content.replace(fault["old"], fault["new"], 1), encoding="utf-8")
