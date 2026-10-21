"""Resolve configuration paths against an explicit trusted directory."""
from pathlib import Path

def resolve_within(root,relative):
    base=Path(root).resolve()
    if not isinstance(relative,str) or not relative or Path(relative).is_absolute(): raise ValueError("path must be relative")
    result=(base/relative).resolve()
    if result!=base and base not in result.parents: raise ValueError("path escapes configuration root")
    return result
