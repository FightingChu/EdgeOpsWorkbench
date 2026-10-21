"""Deterministic most-frequent event attributes with lexical tie breaking."""
from collections import Counter

def top_values(rows,field,limit=10):
    if type(limit) is not int or not 1<=limit<=200: raise ValueError("invalid limit")
    counts=Counter()
    for row in rows:
        value=row.get(field)
        if not isinstance(value,str): raise ValueError("group attribute must be text")
        counts[value]+=1
    return [{"value":value,"count":count} for value,count in sorted(counts.items(),key=lambda item:(-item[1],item[0]))[:limit]]
