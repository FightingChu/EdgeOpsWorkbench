"""Read firmware evidence with bounded bytes and exact descriptor verification."""
from pathlib import Path
import hashlib
from ..domain.deployment.artifacts import describe,Artifact

class ArtifactService:
    def inspect(self,path,version):
        path=Path(path)
        with path.open('rb') as stream: payload=stream.read(16777217)
        if len(payload)>16777216: raise ValueError('firmware exceeds 16777216 bytes')
        return describe(path.name,version,payload)
    def verified_bytes(self,path,artifact):
        if not isinstance(artifact,Artifact): raise ValueError('artifact descriptor required')
        with Path(path).open('rb') as stream: payload=stream.read(artifact.size+1)
        if len(payload)!=artifact.size or hashlib.sha256(payload).hexdigest()!=artifact.sha256: raise ValueError('firmware descriptor does not match bytes')
        return payload
