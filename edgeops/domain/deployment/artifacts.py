"""Firmware artifact descriptors validate digests, sizes, and release identities."""
import hashlib,re
from dataclasses import dataclass

@dataclass(frozen=True)
class Artifact:
    name: str
    version: str
    sha256: str
    size: int
    def __post_init__(self):
        if not isinstance(self.name,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}',self.name): raise ValueError("invalid artifact name")
        if not isinstance(self.version,str) or not re.fullmatch(r'[0-9]{1,6}[.][0-9]{1,6}[.][0-9]{1,6}',self.version): raise ValueError("version must be major.minor.patch")
        if not isinstance(self.sha256,str) or not re.fullmatch('[a-f0-9]{64}',self.sha256): raise ValueError("invalid artifact digest")
        if type(self.size) is not int or not 1<=self.size<=16777216: raise ValueError("artifact size outside bounds")

def describe(name,version,data):
    if not isinstance(data,bytes): raise ValueError("artifact data must be bytes")
    return Artifact(name,version,hashlib.sha256(data).hexdigest(),len(data))
