"""Sliding event frequency evaluates a closed observation interval."""
from ..validation import clock_value,integer

def count_matches(times,now,window,required):
    now=clock_value(now); window=clock_value(window); integer(required,'required',1,100000)
    if window<=0: raise ValueError("window must be positive")
    values=[clock_value(t) for t in times]
    if len(values)>100000 or any(t>now for t in values): raise ValueError("invalid event time series")
    count=sum(now-window<=t<=now for t in values)
    return {"count":count,"firing":count>=required}
