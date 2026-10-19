"""Read-only built-in actions; durable effects are committed by the job worker."""

from ..domain.event_query import EventQuery


def execute(service, action, payload):
    if action == "health.snapshot":
        if payload:
            raise ValueError("health.snapshot accepts no parameters")
        return {"summary": service.summary(), "events": service.list_events(EventQuery(limit=1))["snapshot_id"]}
    if action == "events.query":
        return service.list_events(EventQuery(**payload))
    if action == "incidents.snapshot":
        if payload:
            raise ValueError("incidents.snapshot accepts no parameters")
        return {"incidents": service.list_incidents()[:200]}
    if action == "devices.snapshot":
        if payload:
            raise ValueError("devices.snapshot accepts no parameters")
        return {"devices": service.list_devices()[:200]}
    raise ValueError("unsupported job action: " + str(action))


ACTIONS = ("health.snapshot", "events.query", "incidents.snapshot", "devices.snapshot")
