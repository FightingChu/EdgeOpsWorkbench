"""Bounded newline-delimited JSON adapter rejects malformed tail records."""
import json
from .json_document import decode as decode_array
from ..domain.validation import bounded_json

def decode(text):
    if not isinstance(text,str) or len(text.encode('utf-8'))>8388608: raise ValueError("NDJSON exceeds bounds")
    result=[]
    for line_number,line in enumerate(text.splitlines(),1):
        if not line.strip(): continue
        if len(line.encode('utf-8'))>65536 or len(result)>=10000: raise ValueError("NDJSON record limit exceeded")
        try: result.extend(decode_array('['+line+']'))
        except ValueError as exc: raise ValueError(f"line {line_number}: {exc}") from None
    return result

def encode(rows):
    from .records import normalize
    lines=[]
    for row in rows:
        if len(lines)>=10000: raise ValueError("too many records")
        lines.append(bounded_json(normalize(row)))
    return chr(10).join(lines)+ (chr(10) if lines else '')
