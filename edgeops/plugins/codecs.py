"""Symmetric canonical event codec shared by example importer and exporter."""

import json

from ..application.event_import import MAX_RECORDS, _json_event
from ..domain.events import MAX_RECORD_BYTES


def decode_events(text):
    if not isinstance(text, str) or len(text.encode("utf-8")) > 65536:
        raise ValueError("codec input must be text of at most 65536 bytes")
    result = []
    for line in text.splitlines():
        if not line.strip():
            continue
        if len(line.encode("utf-8")) > MAX_RECORD_BYTES or len(result) >= MAX_RECORDS:
            raise ValueError("codec record limit exceeded")
        result.append(json.loads(_json_event(line).canonical_json()))
    return result


def encode_events(events):
    if not isinstance(events, list) or len(events) > MAX_RECORDS:
        raise ValueError("events must be a bounded list")
    lines = []
    known = {"message", "severity", "service", "device_id", "recorded_at", "kind", "metadata"}
    for event in events:
        if not isinstance(event, dict) or set(event) != known or not isinstance(event["metadata"], dict):
            raise ValueError("export requires canonical event fields")
        if set(event["metadata"]) & known:
            raise ValueError("metadata cannot overwrite canonical event fields")
        value = {**event["metadata"], **{key: event[key] for key in known - {"metadata"}}}
        line = json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)
        _json_event(line)
        lines.append(line)
    return "\n".join(lines) + ("\n" if lines else "")
