"""Alert identities use canonical structured grouping, never concatenated fields."""
import hashlib
from ..validation import bounded_json
from .fields import field

def identity(rule_id,record,group_fields):
    if not isinstance(rule_id,str) or not rule_id or len(rule_id)>128: raise ValueError("invalid rule identity")
    if not isinstance(group_fields,list) or len(group_fields)>8: raise ValueError("invalid grouping fields")
    groups=[field(record,path) for path in group_fields]
    return hashlib.sha256(bounded_json([rule_id,groups]).encode('utf-8')).hexdigest()
