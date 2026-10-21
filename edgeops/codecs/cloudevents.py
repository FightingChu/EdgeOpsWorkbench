"""CloudEvents structured JSON maps identity fields into event metadata."""
import json
from .records import normalize

def decode(text):
    value=json.loads(text)
    if not isinstance(value,dict) or value.get('specversion')!='1.0' or not all(isinstance(value.get(k),str) and value[k] for k in ('id','source','type')): raise ValueError("invalid CloudEvent envelope")
    data=value.get('data')
    if not isinstance(data,dict): raise ValueError("CloudEvent data must be an event object")
    event=normalize(data)
    event['metadata']['cloud_event']={key:value[key] for key in ('id','source','type')}
    return normalize(event)

def encode(event,event_id,source,event_type):
    if not all(isinstance(v,str) and v for v in (event_id,source,event_type)): raise ValueError("CloudEvent identity required")
    return json.dumps({'specversion':'1.0','id':event_id,'source':source,'type':event_type,'data':normalize(event)},ensure_ascii=False,allow_nan=False)
