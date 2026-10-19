"""Periodic check definitions with explicit catch-up semantics."""

from dataclasses import dataclass

from .jobs import JobRequest
from .models import _text
from .validation import integer


@dataclass(frozen=True)
class Schedule:
    name: str
    action: str
    interval: int
    next_run: float
    payload_json: str = "{}"

    def __post_init__(self):
        object.__setattr__(self, "name", _text(self.name, "schedule name", 128))
        integer(self.interval, "interval", 1, 86400 * 30)
        request = JobRequest(self.action, self.payload_json, self.next_run)
        object.__setattr__(self, "action", request.action)
        object.__setattr__(self, "payload_json", request.payload_json)
        object.__setattr__(self, "next_run", request.due_at)
