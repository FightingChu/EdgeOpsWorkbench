"""Redact secrets and machine paths from exported evidence metadata."""

import re

_SECRET = re.compile(r"(?i)(token|secret|password|api[_-]?key)(\s*[:=]\s*)[^,;\s]+")
_PATH = re.compile(r"(?i)([a-z]:\\|/home/|/Users/)[^\s,;]+")


def redact_text(value):
    if not isinstance(value, str):
        raise ValueError("redaction input must be text")
    return _PATH.sub("<path>", _SECRET.sub(r"\1\2<redacted>", value))


def redact_metadata(value):
    if isinstance(value, dict):
        return {str(key): redact_metadata(item) for key, item in value.items() if str(key).lower() not in {"password", "secret", "token", "api_key", "path", "filepath", "file_path"}}
    if isinstance(value, list):
        return [redact_metadata(item) for item in value]
    return redact_text(value) if isinstance(value, str) else value
