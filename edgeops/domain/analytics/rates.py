"""Per-second rate calculations for irregular sampling intervals."""
from .samples import numbers

def rates(times, values):
    ts, vs = numbers(times,2), numbers(values,2)
    if len(ts)!=len(vs): raise ValueError("series lengths differ")
    if any(b<=a for a,b in zip(ts,ts[1:])): raise ValueError("times must increase strictly")
    return [(b-a)/(end-start) for start,end,a,b in zip(ts,ts[1:],vs,vs[1:])]
