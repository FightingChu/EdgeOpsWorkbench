"""Incremental length-prefixed records retain partial input between reads."""
import struct

def encode(records):
    output=bytearray()
    for record in records:
        if not isinstance(record,bytes) or len(record)>65536: raise ValueError("invalid record size")
        output.extend(struct.pack('!I',len(record))); output.extend(record)
        if len(output)>8388608: raise ValueError("record stream too large")
    return bytes(output)

class Decoder:
    def __init__(self): self.buffer=bytearray()
    def feed(self,data):
        if not isinstance(data,bytes) or len(data)+len(self.buffer)>8388608: raise ValueError("invalid record input")
        self.buffer.extend(data); result=[]
        while len(self.buffer)>=4:
            size=struct.unpack('!I',self.buffer[:4])[0]
            if size>65536: raise ValueError("record exceeds limit")
            if len(self.buffer)<4+size: break
            result.append(bytes(self.buffer[4:4+size])); del self.buffer[:4+size]
        return result
    def finish(self):
        if self.buffer: raise ValueError("truncated record stream")
