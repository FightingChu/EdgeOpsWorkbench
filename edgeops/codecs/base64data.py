"""Strict base64 binary transfer with explicit output-size limits."""
import base64,binascii

def encode(data):
    if not isinstance(data,bytes) or len(data)>8388608: raise ValueError("binary payload outside bounds")
    return base64.b64encode(data).decode('ascii')

def decode(text,max_bytes=8388608):
    if type(max_bytes) is not int or not 0<=max_bytes<=8388608: raise ValueError("invalid size limit")
    if not isinstance(text,str) or len(text)>4*((max_bytes+2)//3): raise ValueError("base64 input exceeds limit")
    try: data=base64.b64decode(text,validate=True)
    except (ValueError,binascii.Error): raise ValueError("invalid base64") from None
    if len(data)>max_bytes: raise ValueError("decoded data exceeds limit")
    return data
