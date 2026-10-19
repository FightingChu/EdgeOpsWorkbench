"""Explicit target profiles keep path, timezone, and stale-write policy visible."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ClientProfile:
    name: str
    timezone: str
    encoding: str
    max_cached_events: int
    stale_write_policy: str


profiles = {
    "local": ClientProfile("local", "UTC", "utf-8", 500, "reject"),
    "target-win": ClientProfile("target-win", "Asia/Shanghai", "gb18030", 200, "reject"),
    "target-linux": ClientProfile("target-linux", "UTC", "utf-8", 200, "reject"),
}


def get_profile(name):
    try:
        return profiles[name]
    except KeyError:
        raise ValueError("unknown client profile") from None
