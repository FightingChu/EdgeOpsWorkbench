"""CEF header decoder handles escaped pipes and extension key/value data."""

def decode(text):
    if not isinstance(text,str) or not text.startswith('CEF:') or len(text)>65536: raise ValueError("invalid CEF record")
    parts=[]; current=[]; escaped=False
    for char in text[4:]:
        if escaped: current.append(char); escaped=False
        elif char==chr(92): escaped=True
        elif char=='|' and len(parts)<7: parts.append(''.join(current)); current=[]
        else: current.append(char)
    if escaped: raise ValueError("trailing CEF escape")
    parts.append(''.join(current))
    if len(parts)!=8 or parts[0]!='0' or not parts[6].isdecimal() or not 0<=int(parts[6])<=10: raise ValueError("invalid CEF header")
    return dict(zip(('version','vendor','product','device_version','signature','name','severity','extension'),parts))
