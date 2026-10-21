"""Exclusive event exports use complete serialized bytes before creating the target."""
import hashlib
from pathlib import Path
from ..codecs import json_document,csv_events,ndjson
from ..domain.event_query import EventQuery

def write_events(rows,destination,format='ndjson'):
    encoders={'json':json_document.encode,'csv':csv_events.encode,'ndjson':ndjson.encode}
    if format not in encoders: raise ValueError('unsupported export format')
    payload=encoders[format](rows).encode('utf-8')
    if len(payload)>8388608: raise ValueError('export exceeds 8388608 bytes')
    target=Path(destination)
    try:
        with target.open('xb') as stream: stream.write(payload)
    except FileExistsError: raise ValueError('export destination already exists') from None
    return {'destination':str(target.resolve()),'bytes':len(payload),'sha256':hashlib.sha256(payload).hexdigest()}

class ExportService:
    def __init__(self,operations): self.operations=operations
    def export(self,destination,format='ndjson',limit=10000):
        from ..domain.validation import integer
        integer(limit,'limit',1,10000)
        rows=[]; cursor=None
        while True:
            page=self.operations.list_events(EventQuery(limit=min(200,limit-len(rows)),cursor=cursor))
            for event in page['events']:
                rows.append({key:event[key] for key in ('message','severity','service','device_id','recorded_at','kind','metadata')})
            cursor=page['next_cursor']
            if not cursor or len(rows)>=limit: break
        return {'records':len(rows),'next_cursor':cursor,**write_events(rows,destination,format)}
