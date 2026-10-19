"""Redacted aggregate output for operator-provided records."""

from collections import Counter


def invoke(request):
    if not isinstance(request, dict) or set(request) != {"events"} or not isinstance(request["events"], list) or len(request["events"]) > 200:
        raise ValueError("count-diagnostic requires at most 200 events")
    events = request["events"]
    for event in events:
        if not isinstance(event, dict) or not all(isinstance(event.get(key), str) for key in ("severity", "service")):
            raise ValueError("each event requires text severity and service")
    return {"count": len(events), "severities": dict(Counter(event["severity"] for event in events)),
            "services": dict(Counter(event["service"] for event in events))}
