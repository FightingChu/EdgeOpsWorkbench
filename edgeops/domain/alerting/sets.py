"""Bounded attribute membership with type-aware equality."""

def member(actual,values,negate=False):
    if not isinstance(values,list) or not 1<=len(values)<=100: raise ValueError("membership set must contain 1-100 entries")
    if any(not isinstance(v,(str,int,float,bool,type(None))) for v in values): raise ValueError("membership entries must be scalar")
    found=any(type(actual) is type(value) and actual==value for value in values)
    return not found if negate else found
