"""Interpolated percentiles with exact endpoint semantics."""
from .samples import numbers

def percentile(values, percent):
    data = sorted(numbers(values))
    if isinstance(percent, bool) or not isinstance(percent, (int, float)) or not 0 <= percent <= 100:
        raise ValueError("percent must be between zero and one hundred")
    position = (len(data) - 1) * percent / 100
    left = int(position)
    right = min(left + 1, len(data) - 1)
    fraction = position - left
    return data[left] * (1 - fraction) + data[right] * fraction
