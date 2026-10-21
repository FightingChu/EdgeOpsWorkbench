"""Severity ordering is shared with normalized event inputs."""
from ..events import SEVERITIES

def at_least(actual,minimum):
    if actual not in SEVERITIES or minimum not in SEVERITIES: raise ValueError("unknown severity")
    return SEVERITIES.index(actual)>=SEVERITIES.index(minimum)
