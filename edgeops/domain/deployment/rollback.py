"""Rollback records require a verified previous artifact and explicit device scope."""
import hashlib
from .artifacts import Artifact

def rollback_plan(device_id,previous,data,current_version):
    if not isinstance(device_id,str) or not device_id or not isinstance(previous,Artifact) or not isinstance(data,bytes): raise ValueError("invalid rollback request")
    if len(data)!=previous.size or hashlib.sha256(data).hexdigest()!=previous.sha256: raise ValueError("rollback artifact integrity failed")
    from .compatibility import version_tuple
    if version_tuple(current_version)==version_tuple(previous.version): raise ValueError("device already runs rollback version")
    return {'device_id':device_id,'from_version':current_version,'to_version':previous.version,'sha256':previous.sha256,'bytes':len(data)}
