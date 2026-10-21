"""Normalize imported event mappings through the existing event domain contract."""
import json
from ..domain.events import Event
from ..domain.validation import bounded_json

def normalize(value):
    if not isinstance(value,dict): raise ValueError("event record must be an object")
    known={'message','severity','service','device_id','recorded_at','kind','metadata'}
    metadata=value.get('metadata',{})
    if not isinstance(metadata,dict): raise ValueError("metadata must be an object")
    extras={key:item for key,item in value.items() if key not in known}
    if set(extras)&set(metadata): raise ValueError("metadata conflicts with extra fields")
    event=Event(message=value.get('message'),severity=value.get('severity','info'),service=value.get('service','default'),device_id=value.get('device_id'),recorded_at=value.get('recorded_at'),kind=value.get('kind','log'),metadata_json=bounded_json({**metadata,**extras}))
    return json.loads(event.canonical_json())
