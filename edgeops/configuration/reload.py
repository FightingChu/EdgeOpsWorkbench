"""Configuration revisions compare canonical content and protect running state."""
from copy import deepcopy
import hashlib
from ..domain.validation import bounded_json
from .schema import validate

class ConfigRevision:
    def __init__(self,values):
        self.values=validate(deepcopy(values)); self.generation=1
    @property
    def fingerprint(self):
        return hashlib.sha256(bounded_json(self.values).encode('utf-8')).hexdigest()
    def update(self,values):
        candidate=validate(deepcopy(values))
        if candidate==self.values: return False
        self.values=candidate; self.generation+=1
        return True
