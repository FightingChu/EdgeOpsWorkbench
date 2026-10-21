"""Firmware transfer chunks carry offsets and hashes and assemble without gaps."""
import hashlib

def split(data,chunk_size=4096):
    if not isinstance(data,bytes) or not 1<=len(data)<=16777216 or type(chunk_size) is not int or not 1<=chunk_size<=65536: raise ValueError("invalid chunk input")
    return [{'offset':offset,'data':data[offset:offset+chunk_size],'sha256':hashlib.sha256(data[offset:offset+chunk_size]).hexdigest()} for offset in range(0,len(data),chunk_size)]

def assemble(chunks,expected_size):
    if type(expected_size) is not int or not 1<=expected_size<=16777216: raise ValueError("invalid expected size")
    result=bytearray()
    for chunk in chunks:
        data=chunk.get('data')
        if type(chunk.get('offset')) is not int or chunk['offset']!=len(result) or not isinstance(data,bytes) or not data or len(data)>65536: raise ValueError("chunk offset gap or overlap")
        if hashlib.sha256(data).hexdigest()!=chunk.get('sha256'): raise ValueError("chunk checksum mismatch")
        result.extend(data)
        if len(result)>expected_size: raise ValueError("transfer exceeds expected size")
    if len(result)!=expected_size: raise ValueError("truncated firmware transfer")
    return bytes(result)
