"""Threshold hysteresis avoids alert flapping near the trigger boundary."""
from ..analytics.samples import numbers

def active(value,trigger,recover,was_active=False):
    value,trigger,recover=numbers([value,trigger,recover])
    if recover>=trigger: raise ValueError("recovery threshold must be below trigger")
    if type(was_active) is not bool: raise ValueError("state must be boolean")
    return value>recover if was_active else value>=trigger
