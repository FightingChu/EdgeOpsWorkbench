"""Strict scalar conversion avoids truthy strings and bool/integer confusion."""
import re
import math

def parse_scalar(value,kind):
    if kind=='string':
        if not isinstance(value,str): raise ValueError("expected text")
        return value
    if kind=='boolean':
        if type(value) is bool: return value
        if value in ('true','false'): return value=='true'
        raise ValueError("expected true or false")
    if kind=='integer':
        if type(value) is int: return value
        if isinstance(value,str) and re.fullmatch(r'-?[0-9]{1,18}',value): return int(value)
        raise ValueError("expected an integer")
    if kind=='number':
        if isinstance(value,bool): raise ValueError("boolean is not a number")
        try: result=float(value)
        except (ValueError,TypeError): raise ValueError("expected a finite number") from None
        if not math.isfinite(result): raise ValueError("expected a finite number")
        return result
    raise ValueError("unknown scalar kind")
