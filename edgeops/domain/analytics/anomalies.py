"""Median absolute deviation flags with zero-dispersion handling."""
import statistics
from .samples import numbers

def detect(values, threshold=3.5):
    data = numbers(values)
    if isinstance(threshold,bool) or not isinstance(threshold,(int,float)) or not 0 < threshold <= 100:
        raise ValueError("threshold must be positive and bounded")
    center = statistics.median(data)
    mad = statistics.median(abs(x-center) for x in data)
    indices = [i for i,x in enumerate(data) if (abs(x-center)>0 if mad==0 else .6745*abs(x-center)/mad>threshold)]
    return {"median": center, "mad": mad, "indices": indices}
