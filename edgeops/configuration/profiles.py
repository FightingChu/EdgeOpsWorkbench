"""Named configuration profiles overlay a single validated base object."""
from .merging import merge_layers
from .schema import validate

def select_profile(document,name):
    if not isinstance(document,dict) or set(document)!={'base','profiles'} or not isinstance(document['profiles'],dict): raise ValueError("invalid profile document")
    if name not in document['profiles']: raise ValueError("profile not found")
    return validate(merge_layers(document['base'],document['profiles'][name]))
