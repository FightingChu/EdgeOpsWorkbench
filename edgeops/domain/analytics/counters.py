"""Monotonic counter deltas with explicit device reset accounting."""
from .samples import numbers

def counter_deltas(values, modulus=None):
    data = numbers(values)
    if any(x<0 for x in data): raise ValueError("counters cannot be negative")
    if modulus is not None and (type(modulus) is not int or modulus<=0 or any(x>=modulus for x in data)):
        raise ValueError("counter outside modulus")
    deltas=[]; resets=0
    for before,after in zip(data,data[1:]):
        if after>=before: deltas.append(after-before)
        elif modulus is not None: deltas.append(modulus-before+after)
        else: deltas.append(after); resets+=1
    return {"deltas": deltas, "resets": resets, "total": sum(deltas)}
