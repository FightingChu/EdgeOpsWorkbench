"""Notification cooldown accepts injectable clocks and rejects time reversal."""
from ..validation import clock_value

def eligible(now,last_sent,seconds):
    now=clock_value(now); seconds=clock_value(seconds)
    if last_sent is None: return True
    last=clock_value(last_sent)
    if now<last: raise ValueError("clock moved backwards")
    return now-last>=seconds
