"""Availability from merged outage intervals, clipped to the observation window."""
from .samples import numbers

def availability(start,end,outages):
    start,end=numbers([start,end])
    if end<=start: raise ValueError("observation window must be positive")
    spans=[]
    for span in outages:
        a,b=numbers(span,2)
        if b<a: raise ValueError("outage end precedes start")
        a,b=max(start,a),min(end,b)
        if a<b: spans.append((a,b))
    merged=[]
    for a,b in sorted(spans):
        if merged and a<=merged[-1][1]: merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
        else: merged.append((a,b))
    downtime=sum(b-a for a,b in merged)
    return {"downtime":downtime,"uptime":end-start-downtime,"ratio":1-downtime/(end-start)}
