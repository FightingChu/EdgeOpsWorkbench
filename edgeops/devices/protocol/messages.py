"""Canonical JSON message payloads for device readings and acknowledgements."""

from dataclasses import dataclass
import json

from ...domain import TelemetryReading
from ...domain.validation import bounded_json
from .framing import Frame

READING = 1
ACK = 2


@dataclass(frozen=True)
class ReadingMessage:
    reading: TelemetryReading
    sequence: int

    def __post_init__(self):
        if type(self.sequence) is not int or not 0 <= self.sequence <= 0xffffffff:
            raise ValueError("sequence must be a uint32")


def encode_message(message):
    if not isinstance(message, ReadingMessage):
        raise TypeError("message must be a ReadingMessage")
    payload = {"sequence": message.sequence, "device_id": message.reading.device_id,
               "metric": message.reading.metric, "value": message.reading.value,
               "unit": message.reading.unit, "recorded_at": message.reading.recorded_at}
    return Frame(READING, bounded_json(payload, limit=4096).encode("utf-8"))


def decode_message(frame):
    if not isinstance(frame, Frame):
        raise TypeError("frame must be a Frame")
    try:
        value = json.loads(frame.payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ValueError("message payload must be UTF-8 JSON") from None
    if frame.message_type != READING or not isinstance(value, dict) or set(value) != {"sequence", "device_id", "metric", "value", "unit", "recorded_at"}:
        raise ValueError("unsupported or malformed message")
    return ReadingMessage(TelemetryReading(value["device_id"], value["metric"], value["value"], value["unit"], value["recorded_at"]), value["sequence"])
