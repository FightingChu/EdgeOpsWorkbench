"""JSONL importer that converts text requests into normalized event values."""

from edgeops.plugins.codecs import decode_events


def invoke(request):
    if not isinstance(request, dict) or set(request) != {"text"}:
        raise ValueError("import-jsonl requires a text field")
    return {"events": decode_events(request["text"])}
