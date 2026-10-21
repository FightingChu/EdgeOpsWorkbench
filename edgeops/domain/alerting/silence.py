"""Scoped maintenance silences use start-inclusive end-exclusive time windows."""
from ..validation import clock_value

def is_silenced(rule_id,device_id,now,silences):
    now=clock_value(now)
    if len(silences)>1000: raise ValueError("too many silences")
    for item in silences:
        start,end=clock_value(item['start']),clock_value(item['end'])
        if end<=start: raise ValueError("invalid silence window")
        scoped=item.get('rule_id') in (None,rule_id) and item.get('device_id') in (None,device_id)
        if scoped and start<=now<end: return True
    return False
