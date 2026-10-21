"""JSON document import/export with strict constants and duplicate key rejection."""
import json
from .records import normalize
from ..domain.validation import bounded_json

def _pairs(pairs):
    result={}
    for key,value in pairs:
        if key in result: raise ValueError("duplicate JSON field")
        result[key]=value
    return result

def decode(text):
    if not isinstance(text,str) or len(text.encode('utf-8'))>8388608: raise ValueError("JSON document exceeds bounds")
    def invalid(value): raise ValueError("invalid JSON constant")
    try: value=json.loads(text,object_pairs_hook=_pairs,parse_constant=invalid)
    except (RecursionError,UnicodeError): raise ValueError("invalid JSON document") from None
    if not isinstance(value,list) or len(value)>10000: raise ValueError("JSON document must contain an event list")
    return [normalize(row) for row in value]

def encode(rows):
    values=[normalize(row) for row in rows]
    if len(values)>10000: raise ValueError("too many events")
    return bounded_json(values,limit=8388608)
