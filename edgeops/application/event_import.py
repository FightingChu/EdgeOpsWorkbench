"""Strict, bounded binary file readers that retain physical source coordinates."""

import codecs
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

from ..domain.events import Event, MAX_RECORD_BYTES


MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_RECORDS = 10000
ENCODINGS = {"utf-8", "utf-8-sig", "gb18030", "cp1252"}


@dataclass(frozen=True)
class SourceRecord:
    event: Event
    physical_line: int
    byte_offset: int
    byte_length: int
    raw_record: str


@dataclass(frozen=True)
class ParsedImport:
    source: str
    format: str
    encoding: str
    sha256: str
    byte_count: int
    physical_lines: int
    records: tuple


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError(f"invalid JSON constant: {value}")


def _json_event(text):
    value = json.loads(text, object_pairs_hook=_object, parse_constant=_invalid_constant)
    if not isinstance(value, dict):
        raise ValueError("JSONL record must be an object")
    required = {"message", "severity", "recorded_at"}
    missing = required - value.keys()
    if missing:
        raise ValueError("missing fields: " + ", ".join(sorted(missing)))
    if value["recorded_at"] is None:
        raise ValueError("JSONL recorded_at must include a timezone")
    known = required | {"device_id", "service", "kind"}
    return Event(
        message=value["message"], severity=value["severity"], recorded_at=value["recorded_at"],
        device_id=value.get("device_id"), service=value.get("service", "default"),
        kind=value.get("kind", "log"), metadata_json=json.dumps(
            {key: item for key, item in value.items() if key not in known},
            ensure_ascii=False, allow_nan=False,
        ),
    )


def parse_event_file(path, *, format="jsonl", encoding="utf-8"):
    if format not in {"jsonl", "text"}:
        raise ValueError("format must be jsonl or text")
    try:
        encoding = codecs.lookup(encoding).name
    except (LookupError, TypeError):
        raise ValueError("unsupported encoding") from None
    if encoding not in ENCODINGS:
        raise ValueError("encoding must be utf-8, utf-8-sig, gb18030, or cp1252")
    source = Path(path).resolve()
    digest = hashlib.sha256()
    offset = 0
    line_number = 0
    records = []
    with source.open("rb") as stream:
        while True:
            raw = stream.readline(MAX_RECORD_BYTES + 1)
            if not raw:
                break
            line_number += 1
            if len(raw) > MAX_RECORD_BYTES:
                raise ValueError(f"{source}: line {line_number}, byte {offset}: record exceeds {MAX_RECORD_BYTES} bytes")
            if offset + len(raw) > MAX_FILE_BYTES:
                raise ValueError(f"source exceeds {MAX_FILE_BYTES} bytes at line {line_number}")
            digest.update(raw)
            try:
                # A BOM is a file prefix, never a prefix stripped from every record.
                codec = "utf-8" if encoding == "utf-8-sig" and line_number > 1 else encoding
                text = raw.decode(codec).removesuffix("\n").removesuffix("\r")
                if text.strip():
                    if len(records) >= MAX_RECORDS:
                        raise ValueError(f"source exceeds {MAX_RECORDS} records")
                    event = _json_event(text) if format == "jsonl" else Event(message=text, service="text")
                    records.append(SourceRecord(event, line_number, offset, len(raw), text))
            except (ValueError, TypeError, RecursionError) as exc:
                raise ValueError(f"{source}: line {line_number}, byte {offset}: {exc}") from None
            offset += len(raw)
    return ParsedImport(str(source), format, encoding, digest.hexdigest(), offset, line_number, tuple(records))
