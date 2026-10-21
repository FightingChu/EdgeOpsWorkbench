"""Line-oriented key/value adapter preserves delimiters inside values."""

def decode(text):
    if not isinstance(text,str) or len(text)>65536: raise ValueError("key/value input exceeds bounds")
    result={}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith('#'): continue
        if '=' not in line: raise ValueError("key/value line lacks delimiter")
        key,value=line.split('=',1); key=key.strip()
        if not key or key in result: raise ValueError("empty or duplicate key")
        result[key]=value.strip()
    return result

def encode(values):
    lines=[]
    for key,value in sorted(values.items()):
        if not isinstance(key,str) or not key or '=' in key or any(c in str(key)+str(value) for c in (chr(13),chr(10))): raise ValueError("invalid key/value content")
        lines.append(key+'='+str(value))
    return chr(10).join(lines)
