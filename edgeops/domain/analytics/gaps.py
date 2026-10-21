"""Missing-reading interval detection without filling synthetic telemetry."""
from .samples import numbers

def find_gaps(times, expected_interval, tolerance=0):
    ts=numbers(times)
    interval=numbers([expected_interval])[0]; slack=numbers([tolerance])[0]
    if interval<=0 or slack<0: raise ValueError("invalid interval or tolerance")
    result=[]
    for a,b in zip(ts,ts[1:]):
        if b<=a: raise ValueError("times must increase strictly")
        if b-a>interval+slack: result.append({"after":a,"before":b,"duration":b-a})
    return result
