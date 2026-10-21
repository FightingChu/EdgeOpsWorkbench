"""Consecutive-match windows reset immediately on a nonmatching reading."""
from ..validation import integer

def advance(previous,matched,required):
    integer(previous,'previous',0,1000000); integer(required,'required',1,1000000)
    if type(matched) is not bool: raise ValueError("match must be boolean")
    count=min(required,previous+1) if matched else 0
    return {"count":count,"firing":count>=required}
