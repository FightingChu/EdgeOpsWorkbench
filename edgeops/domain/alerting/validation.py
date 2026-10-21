"""Versioned alert rule definitions are canonicalized before evaluation."""
from ..validation import bounded_json
from ..events import SEVERITIES

def validate_rule(rule):
    if not isinstance(rule,dict) or set(rule)!={'version','id','condition','group_by','severity'}: raise ValueError("invalid alert rule fields")
    if type(rule['version']) is not int or rule['version']!=1: raise ValueError("unsupported rule version")
    if not isinstance(rule['id'],str) or not 1<=len(rule['id'])<=128: raise ValueError("invalid rule id")
    if rule['severity'] not in SEVERITIES: raise ValueError("invalid rule severity")
    if not isinstance(rule['condition'],dict) or not rule['condition']: raise ValueError("missing condition")
    if not isinstance(rule['group_by'],list) or len(rule['group_by'])>8 or not all(isinstance(x,str) for x in rule['group_by']): raise ValueError("invalid grouping")
    bounded_json(rule,limit=16384)
    return rule
