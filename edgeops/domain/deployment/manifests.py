"""Firmware deployment manifest v1 enforces exact fields and target identity."""
from dataclasses import asdict
from .artifacts import Artifact

def validate_manifest(value):
    if not isinstance(value,dict) or set(value)!={'version','artifact','device_kind','minimum_version'}: raise ValueError("invalid firmware manifest fields")
    if type(value['version']) is not int or value['version']!=1: raise ValueError("unsupported firmware manifest version")
    if not isinstance(value['artifact'],dict) or set(value['artifact'])!={'name','version','sha256','size'}: raise ValueError("invalid artifact descriptor")
    artifact=Artifact(**value['artifact'])
    kind=value['device_kind']
    if not isinstance(kind,str) or not 1<=len(kind)<=64 or not kind.isascii() or not all(c.isalnum() or c in '-_' for c in kind): raise ValueError("invalid target kind")
    from .compatibility import version_tuple
    version_tuple(value['minimum_version'])
    return {'version':1,'artifact':asdict(artifact),'device_kind':kind,'minimum_version':value['minimum_version']}
