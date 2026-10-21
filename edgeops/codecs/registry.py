"""Format registry dispatches bounded event imports through domain normalization."""
from . import json_document,csv_events,ndjson,xml_events,cloudevents,logfmt,keyvalue,syslog
from .records import normalize
DECODERS={'json':json_document.decode,'csv':csv_events.decode,'ndjson':ndjson.decode,'xml':xml_events.decode}

def decode_events(text,format):
    if not isinstance(text,str) or len(text.encode('utf-8'))>8388608: raise ValueError("event input exceeds bounds")
    if format in DECODERS: return DECODERS[format](text)
    if format=='cloudevents': return [cloudevents.decode(text)]
    if format=='syslog': return [syslog.decode(text)]
    if format in ('logfmt','keyvalue'):
        adapter=logfmt.decode if format=='logfmt' else keyvalue.decode
        return [normalize(adapter(text))]
    raise ValueError("unknown event format")

def formats():
    return sorted([*DECODERS,'cloudevents','syslog','logfmt','keyvalue'])
