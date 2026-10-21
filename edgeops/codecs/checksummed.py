"""Checksummed binary envelope detects truncation and payload modification."""
import hashlib,struct,hmac
HEADER=struct.Struct('!4sI')

def encode(data):
    if not isinstance(data,bytes) or len(data)>8388608: raise ValueError("payload outside bounds")
    return HEADER.pack(b'EOB1',len(data))+hashlib.sha256(data).digest()+data

def decode(data):
    if not isinstance(data,bytes) or len(data)<40: raise ValueError("truncated envelope")
    magic,size=HEADER.unpack(data[:8])
    if magic!=b'EOB1' or size>8388608 or len(data)!=40+size: raise ValueError("invalid envelope size or magic")
    payload=data[40:]
    if not hmac.compare_digest(data[8:40],hashlib.sha256(payload).digest()): raise ValueError("envelope checksum mismatch")
    return payload
