"""JSON manifest builder for evidence bundles."""

from dataclasses import asdict
import json

from ..domain.validation import bounded_json
from .evidence import Evidence
from .redaction import redact_metadata


def build_manifest(evidence, metadata=None):
    if not isinstance(evidence, Evidence):
        raise TypeError("evidence must be Evidence")
    value = {"version": 1, "evidence": asdict(evidence), "metadata": redact_metadata(metadata or {})}
    bounded_json(value, limit=65536)
    return value


def dump_manifest(evidence, path, metadata=None):
    Path = __import__("pathlib").Path
    Path(path).write_text(json.dumps(build_manifest(evidence, metadata), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
