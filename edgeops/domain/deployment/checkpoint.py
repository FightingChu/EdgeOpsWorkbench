"""Resumable transfer checkpoints bind byte offsets to the verified prefix hash."""
import hashlib
from ..validation import integer

def create(data,offset):
    if not isinstance(data,bytes): raise ValueError("checkpoint data must be bytes")
    integer(offset,'offset',0,len(data))
    return {'version':1,'offset':offset,'prefix_sha256':hashlib.sha256(data[:offset]).hexdigest(),'artifact_sha256':hashlib.sha256(data).hexdigest()}

def validate(data,checkpoint):
    if not isinstance(checkpoint,dict) or set(checkpoint)!={'version','offset','prefix_sha256','artifact_sha256'} or type(checkpoint['version']) is not int or checkpoint['version']!=1: raise ValueError("invalid checkpoint")
    expected=create(data,checkpoint['offset'])
    if checkpoint!=expected: raise ValueError("checkpoint does not match artifact")
    return checkpoint['offset']
