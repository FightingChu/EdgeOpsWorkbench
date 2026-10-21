"""Pearson correlation with explicit undefined-series errors."""
import math
import statistics
from .samples import numbers

def correlate(x,y):
    xs,ys=numbers(x,2),numbers(y,2)
    if len(xs)!=len(ys): raise ValueError("series lengths differ")
    xm,ym=statistics.mean(xs),statistics.mean(ys)
    xx=math.fsum((v-xm)**2 for v in xs); yy=math.fsum((v-ym)**2 for v in ys)
    if xx==0 or yy==0: raise ValueError("constant series has undefined correlation")
    return max(-1.0,min(1.0,math.fsum((a-xm)*(b-ym) for a,b in zip(xs,ys))/math.sqrt(xx*yy)))
