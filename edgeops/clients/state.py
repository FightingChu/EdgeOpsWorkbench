"""Offline read cache state machine with explicit stale indicators."""

from dataclasses import dataclass, field


@dataclass
class ClientState:
    online: bool = True
    snapshot_id: int = 0
    events: list = field(default_factory=list)
    stale: bool = False
    pending_writes: list = field(default_factory=list)


def apply_event_page(state, page):
    if not isinstance(state, ClientState) or not isinstance(page, dict) or not isinstance(page.get("events"), list):
        raise ValueError("invalid event page")
    snapshot = page.get("snapshot_id")
    if type(snapshot) is not int or snapshot < state.snapshot_id:
        state.stale = True
        return state
    state.snapshot_id = snapshot
    state.events = list(page["events"])
    state.stale = not state.online
    return state


def queue_write(state, payload):
    if not isinstance(state, ClientState):
        raise TypeError("state must be ClientState")
    state.pending_writes.append(payload)
    state.stale = True


def reconnect(state):
    state.online = True
    state.stale = bool(state.pending_writes)
