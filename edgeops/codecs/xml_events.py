"""XML event adapter prohibits DTD/entity expansion and preserves scalar fields."""
import xml.etree.ElementTree as ET
from .records import normalize

def decode(text):
    if not isinstance(text,str) or len(text)>1048576 or '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper(): raise ValueError("unsafe or oversized XML")
    try: root=ET.fromstring(text)
    except ET.ParseError: raise ValueError("invalid XML") from None
    if root.tag!='events' or len(root)>10000: raise ValueError("invalid events root")
    result=[]
    for node in root:
        if node.tag!='event': raise ValueError("unknown event element")
        fields={}
        for child in node:
            if child.tag in fields or len(child): raise ValueError("duplicate or nested event field")
            fields[child.tag]=child.text or ''
        result.append(normalize(fields))
    return result
