"""Deterministic protocol simulator used by host tests."""

from datetime import datetime, timezone

from ...domain import TelemetryReading
from .framing import encode_frame
from .messages import ReadingMessage, encode_message


def reading_frame(device_id, sequence, value, *, recorded_at=None):
    recorded_at = recorded_at or datetime.now(timezone.utc).isoformat()
    reading = TelemetryReading(device_id, "temperature", value, "C", recorded_at)
    return encode_frame(encode_message(ReadingMessage(reading, sequence)))
