"""Deterministic event values, normalization, and content identity."""

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json

from .models import _text


SEVERITIES = ("debug", "info", "warning", "error", "critical")
MAX_MESSAGE_CHARS = 16384
MAX_RECORD_BYTES = 65536
INGEST_VERSION = 1


def event_timestamp(value):
    if not isinstance(value, str) or len(value) > 64:
        raise ValueError("timestamp must be an ISO-8601 string with a timezone")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError()
        return parsed.astimezone(timezone.utc).isoformat(timespec="microseconds")
    except (ValueError, OverflowError):
        raise ValueError("timestamp must be valid ISO-8601 with a timezone") from None


@dataclass(frozen=True)
class Event:
    message: str
    severity: str = "info"
    service: str = "default"
    device_id: str = None
    recorded_at: str = None
    kind: str = "log"
    metadata_json: str = "{}"

    def __post_init__(self):
        if (not isinstance(self.message, str) or not self.message.strip()
                or len(self.message) > MAX_MESSAGE_CHARS or "\x00" in self.message):
            raise ValueError(f"message must contain 1-{MAX_MESSAGE_CHARS} characters without NUL")
        severity = _text(self.severity, "severity", 16).lower()
        if severity not in SEVERITIES:
            raise ValueError("severity must be one of " + ", ".join(SEVERITIES))
        object.__setattr__(self, "severity", severity)
        object.__setattr__(self, "service", _text(self.service, "service", 128))
        object.__setattr__(self, "kind", _text(self.kind, "kind", 64))
        if self.device_id is not None:
            object.__setattr__(self, "device_id", _text(self.device_id, "device id", 64))
        if self.recorded_at is not None:
            object.__setattr__(self, "recorded_at", event_timestamp(self.recorded_at))
        metadata = json.loads(self.metadata_json)
        if not isinstance(metadata, dict):
            raise ValueError("metadata must be a JSON object")
        object.__setattr__(self, "metadata_json", json.dumps(
            metadata, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ))
        try:
            size = len(self.canonical_json().encode("utf-8"))
        except UnicodeEncodeError:
            raise ValueError("event must contain valid Unicode") from None
        if size > MAX_RECORD_BYTES:
            raise ValueError(f"normalized event exceeds {MAX_RECORD_BYTES} bytes")

    def canonical_json(self):
        return json.dumps({
            "message": self.message, "severity": self.severity, "service": self.service,
            "device_id": self.device_id, "recorded_at": self.recorded_at, "kind": self.kind,
            "metadata": json.loads(self.metadata_json),
        }, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

    @property
    def fingerprint(self):
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()
