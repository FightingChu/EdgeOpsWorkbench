"""Deterministic deployment simulation reports transfer and verification failures accurately."""
import hashlib
from .artifacts import Artifact
from .chunks import split,assemble
from .lifecycle import transition

def simulate(artifact,data,fail_at=None,chunk_size=4096):
    if not isinstance(artifact,Artifact) or fail_at not in (None,'transfer','verify','apply'): raise ValueError("invalid simulation input")
    history=['queued']; received=0
    def move(action): history.append(transition(history[-1],action))
    move('start')
    if fail_at=='transfer': move('fail'); return {'state':history[-1],'history':history,'received_bytes':0,'error':'transfer failed'}
    try: payload=assemble(split(data,chunk_size),artifact.size)
    except ValueError as exc: move('fail'); return {'state':history[-1],'history':history,'received_bytes':0,'error':str(exc)}
    received=len(payload); move('transferred')
    if fail_at=='verify' or hashlib.sha256(payload).hexdigest()!=artifact.sha256:
        move('fail'); return {'state':history[-1],'history':history,'received_bytes':received,'error':'verification failed'}
    move('verified'); move('fail' if fail_at=='apply' else 'applied')
    return {'state':history[-1],'history':history,'received_bytes':received,'error':'apply failed' if fail_at=='apply' else None}
