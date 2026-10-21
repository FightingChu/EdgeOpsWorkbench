"""Duration strings use explicit units and a one-month upper bound."""
import re
from decimal import Decimal

def parse_duration(value):
    if not isinstance(value,str): raise ValueError("duration must be text")
    match=re.fullmatch(r'([0-9]{1,8}(?:[.][0-9]{1,3})?)(ms|s|m|h|d)',value)
    if not match: raise ValueError("invalid duration")
    scale={'ms':Decimal('.001'),'s':1,'m':60,'h':3600,'d':86400}[match[2]]
    result=Decimal(match[1])*scale
    if not 0<result<=2592000: raise ValueError("duration outside bounds")
    return float(result)
