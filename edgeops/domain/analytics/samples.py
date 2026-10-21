"""Bounded finite numeric samples shared by telemetry analytics."""
import math

def numbers(values, minimum=1):
    result = list(values)
    if not minimum <= len(result) <= 100000:
        raise ValueError("sample count outside bounds")
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in result):
        raise ValueError("samples must be finite numbers")
    return [float(x) for x in result]
