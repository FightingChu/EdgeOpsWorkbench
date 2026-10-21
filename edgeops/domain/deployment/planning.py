"""Deterministic rollout planning separates canaries, waves, and blocked devices."""
from .manifests import validate_manifest
from .inventory import normalize_devices
from .compatibility import check
from .policy import RolloutPolicy

def plan(devices,manifest,policy=None):
    manifest=validate_manifest(manifest); devices=normalize_devices(devices); policy=policy or RolloutPolicy()
    eligible=[]; blocked=[]
    for device in devices:
        outcome=check(device,manifest)
        if outcome['compatible']: eligible.append(device['id'])
        else: blocked.append({'device_id':device['id'],'reason':outcome['reason']})
    canaries=eligible[:policy.canary_count]; remaining=eligible[len(canaries):]
    waves=([canaries] if canaries else [])+[remaining[i:i+policy.batch_size] for i in range(0,len(remaining),policy.batch_size)]
    return {'waves':waves,'blocked':blocked,'target_version':manifest['artifact']['version'],'artifact_sha256':manifest['artifact']['sha256']}
