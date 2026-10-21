"""Device/metric rollups keep unrelated telemetry series separate."""
import math
from .samples import numbers

def rollup(rows):
    groups={}
    for index,row in enumerate(rows):
        if index>=100000: raise ValueError("too many rows")
        if not isinstance(row,dict) or not all(isinstance(row.get(k),str) and row[k] for k in ('device_id','metric')):
            raise ValueError("row requires device_id and metric")
        value=numbers([row.get('value')])[0]
        groups.setdefault((row['device_id'],row['metric']),[]).append(value)
    return [{"device_id":d,"metric":m,"count":len(v),"mean":math.fsum(v)/len(v),"min":min(v),"max":max(v)} for (d,m),v in sorted(groups.items())]
