"""Example exporter paired with import-jsonl."""

from edgeops.plugins.codecs import encode_events


def invoke(request):
    if not isinstance(request, dict) or set(request) != {"events"}:
        raise ValueError("export-jsonl requires an events field")
    return {"text": encode_events(request["events"])}
