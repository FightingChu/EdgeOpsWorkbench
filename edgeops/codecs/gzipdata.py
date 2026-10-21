"""Gzip decoding uses a bounded decompressor and rejects concatenated streams."""
import gzip,zlib

def encode(data):
    if not isinstance(data,bytes) or len(data)>8388608: raise ValueError("gzip input outside bounds")
    return gzip.compress(data,mtime=0)

def decode(data,max_bytes=8388608):
    if not isinstance(data,bytes) or len(data)>8388608 or type(max_bytes) is not int or not 0<=max_bytes<=8388608: raise ValueError("invalid gzip bounds")
    decoder=zlib.decompressobj(16+zlib.MAX_WBITS)
    try: result=decoder.decompress(data,max_bytes+1)
    except zlib.error: raise ValueError("invalid gzip stream") from None
    if len(result)>max_bytes or decoder.unconsumed_tail: raise ValueError("gzip output exceeds limit")
    if not decoder.eof or decoder.unused_data: raise ValueError("truncated or concatenated gzip stream")
    return result
