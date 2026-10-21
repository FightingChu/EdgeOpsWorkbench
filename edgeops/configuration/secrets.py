"""Recursive configuration redaction with bounded structural depth."""
import re
SECRET=re.compile(r'(password|secret|token|api[_-]?key|authorization|cookie|credential)',re.I)

def redact(value,depth=0):
    if depth>20: raise ValueError("configuration nesting exceeds limit")
    if isinstance(value,dict): return {key:'<redacted>' if SECRET.search(str(key)) else redact(item,depth+1) for key,item in value.items()}
    if isinstance(value,list): return [redact(item,depth+1) for item in value]
    return value
