"""Configuration inspection returns validated values with secret redaction."""
from ..configuration.loader import load
from ..configuration.secrets import redact
from ..configuration.diff import changes
from ..configuration.profiles import select_profile

class ConfigurationService:
    def inspect(self,paths=(),environment=None,overrides=None):
        return redact(load(paths,environment,overrides))
    def compare(self,before,after):
        from ..configuration.schema import validate
        return changes(redact(validate(before)),redact(validate(after)))
    def profile(self,document,name):
        return redact(select_profile(document,name))
