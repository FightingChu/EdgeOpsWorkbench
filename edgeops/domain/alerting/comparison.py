"""Explicitly typed comparisons prevent accidental string/numeric coercion."""
import math

def compare(actual,operator,expected):
    if operator in ('eq','ne'):
        equal=type(actual) is type(expected) and actual==expected
        return equal if operator=='eq' else not equal
    if operator not in ('gt','ge','lt','le'): raise ValueError("unknown comparison")
    for value in (actual,expected):
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
            raise ValueError("ordered comparison requires finite numbers")
    return {'gt':actual>expected,'ge':actual>=expected,'lt':actual<expected,'le':actual<=expected}[operator]
