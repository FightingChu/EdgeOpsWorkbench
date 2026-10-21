"""Event predicate dispatch keeps field lookup and operator semantics explicit."""
from .fields import field
from .comparison import compare
from .textmatch import match_text
from .severity import at_least
from .sets import member

def evaluate(record,condition):
    if not isinstance(condition,dict) or set(condition)!={'field','op','value'}: raise ValueError("predicate requires field, op, value")
    actual=field(record,condition['field']); op=condition['op']; expected=condition['value']
    if op in ('eq','ne','gt','ge','lt','le'): return compare(actual,op,expected)
    if op in ('contains','prefix','suffix'): return match_text(actual,op,expected)
    if op=='severity': return at_least(actual,expected)
    if op in ('in','not_in'): return member(actual,expected,op=='not_in')
    raise ValueError("unknown predicate operator")
