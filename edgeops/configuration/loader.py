"""Bounded JSON file layers, explicit environment, and CLI overrides."""
import json
from pathlib import Path
from .merging import merge_layers
from .environment import read_environment
from .schema import validate

def load(paths=(),environment=None,overrides=None):
    layers=[]
    for path in paths:
        with Path(path).open('rb') as stream: raw=stream.read(65537)
        if len(raw)>65536: raise ValueError("configuration file exceeds 65536 bytes")
        try: value=json.loads(raw.decode('utf-8-sig'))
        except (UnicodeError,ValueError): raise ValueError("invalid configuration JSON") from None
        layers.append(value)
    layers.append(read_environment(environment or {})); layers.append(overrides or {})
    return validate(merge_layers(*layers))
