"""Sliding mean with an explicit warm-up output policy."""
from collections import deque
import math
from .samples import numbers

def moving_average(values, window, partial=False):
    if type(window) is not int or not 1 <= window <= 10000:
        raise ValueError("window must be between 1 and 10000")
    data = numbers(values, minimum=0)
    queue = deque(maxlen=window)
    result = []
    for value in data:
        queue.append(value)
        result.append(math.fsum(queue) / len(queue) if partial or len(queue) == window else None)
    return result
