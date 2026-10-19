"""Shared bounds for durable JSON contracts and injected clock values."""

import json
import math


def bounded_json(value, *, limit=65536):
    try:
        result = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
        if len(result.encode("utf-8")) > limit:
            raise ValueError(f"JSON payload exceeds {limit} bytes")
        return result
    except (TypeError, UnicodeError, RecursionError) as exc:
        raise ValueError(f"invalid JSON payload: {exc}") from None


def clock_value(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0 or value > 253402300799:
        raise ValueError("clock value must be finite seconds since epoch")
    return float(value)


def integer(value, name, minimum, maximum):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{name} must be an integer between {minimum} and {maximum}")
    return value
