"""Bounded filters and snapshot cursors for immutable events."""

import base64
import binascii
from dataclasses import dataclass
import hashlib
import json

from .events import SEVERITIES, event_timestamp
from .models import _text


@dataclass(frozen=True)
class EventQuery:
    limit: int = 50
    cursor: str = None
    q: str = None
    severity: str = None
    service: str = None
    device_id: str = None
    since: str = None
    until: str = None

    def __post_init__(self):
        if type(self.limit) is not int or not 1 <= self.limit <= 200:
            raise ValueError("limit must be an integer between 1 and 200")
        for name, length in (("q", 256), ("service", 128), ("device_id", 64)):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, _text(value, name, length))
        if self.severity is not None and self.severity not in SEVERITIES:
            raise ValueError("invalid severity")
        for name in ("since", "until"):
            if getattr(self, name) is not None:
                object.__setattr__(self, name, event_timestamp(getattr(self, name)))
        if self.since and self.until and self.since > self.until:
            raise ValueError("since must be before or equal to until")
        if self.cursor is not None:
            self.position()

    def filter_key(self):
        values = {name: getattr(self, name) for name in
                  ("q", "severity", "service", "device_id", "since", "until")}
        return hashlib.sha256(json.dumps(values, sort_keys=True).encode("utf-8")).hexdigest()

    def next_cursor(self, snapshot, before):
        payload = json.dumps([1, snapshot, before, self.filter_key()], separators=(",", ":"))
        return base64.urlsafe_b64encode(payload.encode("ascii")).decode("ascii").rstrip("=")

    def position(self):
        if self.cursor is None:
            return None
        try:
            if not isinstance(self.cursor, str) or not 1 <= len(self.cursor) <= 512:
                raise ValueError()
            decoded = base64.b64decode(self.cursor + "=" * (-len(self.cursor) % 4),
                                       altchars=b"-_", validate=True)
            version, snapshot, before, key = json.loads(decoded)
            if (type(version) is not int or version != 1
                    or type(snapshot) is not int or type(before) is not int
                    or not 0 < before <= snapshot <= 9223372036854775807
                    or key != self.filter_key()):
                raise ValueError()
            return snapshot, before
        except (ValueError, TypeError, binascii.Error, UnicodeError):
            raise ValueError("invalid cursor or cursor does not match filters") from None
