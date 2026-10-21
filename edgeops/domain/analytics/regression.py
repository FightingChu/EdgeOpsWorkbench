"""Least-squares trend fit with constant-input detection."""
import math
from .samples import numbers

def fit(x, y):
    xs, ys = numbers(x, 2), numbers(y, 2)
    if len(xs) != len(ys): raise ValueError("series lengths differ")
    xm, ym = math.fsum(xs)/len(xs), math.fsum(ys)/len(ys)
    denominator = math.fsum((v-xm)**2 for v in xs)
    if denominator == 0: raise ValueError("x series must vary")
    slope = math.fsum((a-xm)*(b-ym) for a,b in zip(xs,ys))/denominator
    return {"slope": slope, "intercept": ym-slope*xm}
