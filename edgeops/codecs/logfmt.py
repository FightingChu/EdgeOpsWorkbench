"""Strict logfmt tokens retain quoted spaces, equals signs, and escapes."""
import shlex
import json

def decode(text):
    if not isinstance(text,str) or len(text)>65536: raise ValueError("logfmt input too large")
    result={}
    try: tokens=shlex.split(text,posix=True)
    except ValueError: raise ValueError("invalid logfmt quoting") from None
    for token in tokens:
        if '=' not in token: raise ValueError("logfmt token requires equals")
        key,value=token.split('=',1)
        if not key or key in result or len(result)>=100: raise ValueError("invalid or duplicate logfmt key")
        result[key]=value
    return result

def encode(values):
    if not isinstance(values,dict) or len(values)>100: raise ValueError("invalid logfmt mapping")
    tokens=[]
    for key,value in sorted(values.items()):
        if not isinstance(key,str) or not key or any(c.isspace() or c in '=\"' for c in key): raise ValueError("invalid logfmt key")
        tokens.append(key+'='+json.dumps(str(value),ensure_ascii=False))
    return ' '.join(tokens)
