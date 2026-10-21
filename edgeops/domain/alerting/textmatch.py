"""Bounded literal message matching without regex execution."""

def match_text(actual,operator,expected,case_sensitive=True):
    if not isinstance(actual,str) or not isinstance(expected,str) or len(expected)>256 or len(actual)>65536:
        raise ValueError("text outside matching bounds")
    if not case_sensitive: actual,expected=actual.casefold(),expected.casefold()
    if operator=='contains': return expected in actual
    if operator=='prefix': return actual.startswith(expected)
    if operator=='suffix': return actual.endswith(expected)
    raise ValueError("unknown text operator")
