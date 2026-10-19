"""Validated domain inputs."""

from dataclasses import dataclass
from datetime import datetime
import math


def _text(value, label, limit=128):
    if not isinstance(value, str):
        raise ValueError(f"{label} must be text")
    value = value.strip()
    if not value or len(value) > limit or any(ord(char) < 32 for char in value):
        raise ValueError(f"{label} must contain 1-{limit} printable characters")
    return value


def _timestamp(value):
    if not isinstance(value, str):
        raise ValueError("recorded_at must be an ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("recorded_at must be a valid ISO-8601 timestamp") from None
    if parsed.tzinfo is None:
        raise ValueError("recorded_at must include a timezone")
    return parsed.isoformat()


@dataclass(frozen=True)
class Device:
    id: str
    name: str
    kind: str

    def __post_init__(self):
        object.__setattr__(self, "id", _text(self.id, "device id", 64))
        object.__setattr__(self, "name", _text(self.name, "device name"))
        object.__setattr__(self, "kind", _text(self.kind, "device kind", 64))


@dataclass(frozen=True)
class TelemetryReading:
    device_id: str
    metric: str
    value: float
    unit: str
    recorded_at: str

    def __post_init__(self):
        object.__setattr__(self, "device_id", _text(self.device_id, "device id", 64))
        object.__setattr__(self, "metric", _text(self.metric, "metric", 64).lower())
        if isinstance(self.value, bool) or not isinstance(self.value, (int, float)):
            raise ValueError("value must be numeric")
        numeric = float(self.value)
        if not math.isfinite(numeric):
            raise ValueError("value must be finite")
        object.__setattr__(self, "value", numeric)
        object.__setattr__(self, "unit", _text(self.unit, "unit", 24))
        object.__setattr__(self, "recorded_at", _timestamp(self.recorded_at))

