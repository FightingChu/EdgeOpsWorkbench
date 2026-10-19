"""Validated job requests and deterministic retry policy."""

from dataclasses import dataclass
import json

from .models import _text
from .validation import bounded_json, clock_value, integer


@dataclass(frozen=True)
class JobRequest:
    action: str
    payload_json: str = "{}"
    due_at: float = 0
    max_attempts: int = 3
    retry_delay: int = 5
    dedup_key: str = None

    def __post_init__(self):
        object.__setattr__(self, "action", _text(self.action, "action", 128))
        payload = json.loads(self.payload_json)
        if not isinstance(payload, dict):
            raise ValueError("job payload must be an object")
        object.__setattr__(self, "payload_json", bounded_json(payload))
        object.__setattr__(self, "due_at", clock_value(self.due_at))
        integer(self.max_attempts, "max_attempts", 1, 10)
        integer(self.retry_delay, "retry_delay", 1, 3600)
        if self.dedup_key is not None:
            object.__setattr__(self, "dedup_key", _text(self.dedup_key, "dedup key", 200))


def backoff(delay, attempt):
    integer(delay, "retry_delay", 1, 3600)
    integer(attempt, "attempt", 1, 10)
    return min(3600, delay * 2 ** (attempt - 1))
