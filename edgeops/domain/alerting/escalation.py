"""Occurrence-based escalation preserves the minimum configured severity."""
from ..events import SEVERITIES
from ..validation import integer

def severity_for(base,occurrences,steps):
    integer(occurrences,'occurrences',1,1000000000)
    if base not in SEVERITIES: raise ValueError("unknown base severity")
    selected=SEVERITIES.index(base)
    for count,level in steps:
        integer(count,'threshold',1,1000000000)
        if level not in SEVERITIES: raise ValueError("unknown escalation severity")
        if occurrences>=count: selected=max(selected,SEVERITIES.index(level))
    return SEVERITIES[selected]
