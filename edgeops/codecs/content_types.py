"""Content type negotiation selects registered event decoders only."""
TYPES={'application/json':'json','application/x-ndjson':'ndjson','text/csv':'csv','application/xml':'xml','application/cloudevents+json':'cloudevents'}

def resolve(content_type):
    if not isinstance(content_type,str) or len(content_type)>256: raise ValueError("invalid content type")
    parts=[part.strip() for part in content_type.split(';')]; media=parts[0].lower()
    if media not in TYPES: raise ValueError("unsupported content type")
    for param in parts[1:]:
        if '=' not in param: raise ValueError("invalid media parameter")
        key,value=param.split('=',1)
        if key.lower()=='charset' and value.strip('"').lower() not in ('utf-8','utf8'): raise ValueError("event interchange requires UTF-8")
    return TYPES[media]
