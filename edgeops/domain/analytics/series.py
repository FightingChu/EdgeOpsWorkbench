"""Timestamp ordering and conflict detection for a single numeric series."""
from .samples import numbers

def normalize(points):
    result={}
    for point in points:
        if len(point)!=2: raise ValueError("point must contain timestamp and value")
        timestamp,value=numbers(point,2)
        if timestamp in result and result[timestamp]!=value: raise ValueError("conflicting values at one timestamp")
        result[timestamp]=value
        if len(result)>100000: raise ValueError("series exceeds limit")
    return [{"time":t,"value":v} for t,v in sorted(result.items())]
