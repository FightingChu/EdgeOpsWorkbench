"""Firmware persistence enforces immutable artifact identity and optimistic revisions."""
from .repositories import utc_now
from .audit import record
from ..domain.deployment.lifecycle import transition

def register_artifact(connection,artifact):
    row=connection.execute('SELECT * FROM firmware_artifacts WHERE name=? AND version=?',(artifact.name,artifact.version)).fetchone()
    if row:
        if row['sha256']!=artifact.sha256 or row['size']!=artifact.size: raise ValueError('artifact version already describes different bytes')
        return row['id']
    cursor=connection.execute('INSERT INTO firmware_artifacts(name,version,sha256,size,created_at) VALUES(?,?,?,?,?)',(artifact.name,artifact.version,artifact.sha256,artifact.size,utc_now()))
    record(connection,'firmware.register',cursor.lastrowid,{'sha256':artifact.sha256,'version':artifact.version})
    return cursor.lastrowid

def create(connection,device_id,artifact_id):
    if connection.execute('SELECT 1 FROM devices WHERE id=?',(device_id,)).fetchone() is None: raise ValueError('device not registered')
    if connection.execute('SELECT 1 FROM firmware_artifacts WHERE id=?',(artifact_id,)).fetchone() is None: raise ValueError('artifact not registered')
    cursor=connection.execute("INSERT INTO deployments(device_id,artifact_id,state,revision,created_at,updated_at) VALUES(?,?,'queued',0,?,?)",(device_id,artifact_id,utc_now(),utc_now()))
    record(connection,'deployment.create',cursor.lastrowid,{'device_id':device_id,'artifact_id':artifact_id})
    return cursor.lastrowid

def get(connection,deployment_id):
    row=connection.execute('SELECT d.*,a.size AS artifact_size,a.sha256 AS artifact_sha256,a.version AS artifact_version FROM deployments d JOIN firmware_artifacts a ON a.id=d.artifact_id WHERE d.id=?',(deployment_id,)).fetchone()
    if row is None: return None
    result=dict(row)
    result['history']=[dict(item) for item in connection.execute('SELECT revision,action,from_state,to_state,created_at FROM deployment_transitions WHERE deployment_id=? ORDER BY revision',(deployment_id,))]
    return result

def advance(connection,deployment_id,expected_revision,action,received_bytes=None,error=None):
    row=get(connection,deployment_id)
    if row is None: raise ValueError('deployment not found')
    if type(expected_revision) is not int or row['revision']!=expected_revision: raise ValueError('stale deployment revision')
    target=transition(row['state'],action)
    received=row['received_bytes'] if received_bytes is None else received_bytes
    if type(received) is not int or not row['received_bytes']<=received<=row['artifact_size']: raise ValueError('invalid transfer progress')
    if action=='transferred' and received!=row['artifact_size']: raise ValueError('firmware transfer is incomplete')
    now=utc_now(); revision=expected_revision+1
    connection.execute('UPDATE deployments SET state=?,revision=?,received_bytes=?,error=?,updated_at=? WHERE id=?',(target,revision,received,str(error)[:2048] if error is not None else None,now,deployment_id))
    connection.execute('INSERT INTO deployment_transitions(deployment_id,revision,action,from_state,to_state,created_at) VALUES(?,?,?,?,?,?)',(deployment_id,revision,action,row['state'],target,now))
    record(connection,'deployment.transition',deployment_id,{'action':action,'state':target,'revision':revision})
    return get(connection,deployment_id)
