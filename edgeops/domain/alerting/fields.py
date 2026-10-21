"""Safe dotted-field access for nested event metadata."""
import re

def field(record,path):
    if not isinstance(path,str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*([.][A-Za-z_][A-Za-z0-9_]*){0,15}',path):
        raise ValueError("invalid field path")
    current=record
    for part in path.split('.'):
        if not isinstance(current,dict) or part not in current: raise ValueError("event field missing: "+path)
        current=current[part]
    return current
