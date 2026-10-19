"""A deterministic rule plugin with explicit missing/unknown severity errors."""

from edgeops.domain.events import SEVERITIES


def invoke(request):
    if not isinstance(request, dict) or set(request) != {"events", "minimum"}:
        raise ValueError("severity-rule requires events and minimum")
    minimum = request["minimum"]
    events = request["events"]
    if minimum not in SEVERITIES or not isinstance(events, list) or len(events) > 200:
        raise ValueError("invalid minimum or event count")
    matches = []
    for index, event in enumerate(events):
        if not isinstance(event, dict) or event.get("severity") not in SEVERITIES:
            raise ValueError("each event must contain a known severity")
        if SEVERITIES.index(event["severity"]) >= SEVERITIES.index(minimum):
            matches.append(index)
    return {"matching_indices": matches, "count": len(matches)}
