"""Equal-width histograms whose bins preserve every input sample."""
from .samples import numbers

def histogram(values, bins=10):
    data = numbers(values)
    if type(bins) is not int or not 1 <= bins <= 1000: raise ValueError("invalid bin count")
    low, high = min(data), max(data)
    counts = [0] * bins
    for value in data:
        index = min(bins-1, int((value-low)/(high-low)*bins)) if high>low else 0
        counts[index] += 1
    return {"minimum": low, "maximum": high, "counts": counts}
