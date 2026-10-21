"""Exponentially weighted smoothing for noisy device readings."""
from .samples import numbers

def smooth(values, alpha):
    data = numbers(values)
    if isinstance(alpha, bool) or not isinstance(alpha, (int,float)) or not 0 < alpha <= 1:
        raise ValueError("alpha must be in (0,1]")
    result = [data[0]]
    for value in data[1:]:
        result.append(alpha * value + (1 - alpha) * result[-1])
    return result
