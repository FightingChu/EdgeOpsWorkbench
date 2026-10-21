"""UTC-independent fixed-width bucket aggregation with explicit origin."""
import math
from .samples import numbers

def bucket(times, values, width, origin=0):
    ts,vs=numbers(times),numbers(values)
    size=numbers([width])[0]; start=numbers([origin])[0]
    if len(ts)!=len(vs) or size<=0: raise ValueError("invalid bucket inputs")
    groups={}
    for timestamp,value in zip(ts,vs):
        key=math.floor((timestamp-start)/size)
        groups.setdefault(key,[]).append(value)
    return [{"start":start+k*size,"count":len(v),"mean":math.fsum(v)/len(v)} for k,v in sorted(groups.items())]
