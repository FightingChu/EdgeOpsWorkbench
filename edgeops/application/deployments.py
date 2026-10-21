"""Durable deployment operations commit transitions and audit evidence atomically."""
from dataclasses import asdict
from ..persistence import deployments
from ..domain.deployment.artifacts import Artifact
from ..domain.deployment.simulator import simulate
from ..domain.validation import integer
from .artifacts import ArtifactService

class DeploymentService:
    def __init__(self,operations): self.operations=operations; self.database=operations.database
    def register(self,path,version):
        artifact=ArtifactService().inspect(path,version); self.database.initialize()
        with self.database.connect() as connection:
            connection.execute('BEGIN IMMEDIATE'); identity=deployments.register_artifact(connection,artifact)
        return {'id':identity,**asdict(artifact)}
    def create(self,device_id,artifact_id):
        integer(artifact_id,'artifact_id',1,2**63-1); self.database.initialize()
        with self.database.connect() as connection:
            connection.execute('BEGIN IMMEDIATE'); identity=deployments.create(connection,device_id,artifact_id)
            return deployments.get(connection,identity)
    def get(self,identity):
        integer(identity,'deployment_id',1,2**63-1); self.database.initialize()
        with self.database.connect() as connection: return deployments.get(connection,identity)
    def advance(self,identity,revision,action,received_bytes=None,error=None):
        self.database.initialize()
        with self.database.connect() as connection:
            connection.execute('BEGIN IMMEDIATE')
            return deployments.advance(connection,identity,revision,action,received_bytes,error)
    def run_simulation(self,identity,path,fail_at=None):
        row=self.get(identity)
        if row is None or row['state']!='queued': raise ValueError('simulation requires a queued deployment')
        with self.database.connect() as connection:
            raw=connection.execute('SELECT name,version,sha256,size FROM firmware_artifacts WHERE id=?',(row['artifact_id'],)).fetchone()
        artifact=Artifact(**dict(raw)); payload=ArtifactService().verified_bytes(path,artifact)
        result=simulate(artifact,payload,fail_at)
        current=self.advance(identity,row['revision'],'start')
        for state in result['history'][2:]:
            action={'verifying':'transferred','applying':'verified','succeeded':'applied','failed':'fail'}[state]
            current=self.advance(identity,current['revision'],action,received_bytes=result['received_bytes'],error=result['error'] if state=='failed' else None)
        return current
