"""Environment overlays accept a fixed allowlist instead of importing process secrets."""
from .scalar import parse_scalar

def read_environment(values,prefix='EDGEOPS_'):
    mapping={'HOST':('host','string'),'PORT':('port','integer'),'DATA_DIR':('data_dir','string'),'DATABASE_NAME':('database_name','string')}
    result={}
    for name,(field,kind) in mapping.items():
        key=prefix+name
        if key in values: result[field]=parse_scalar(values[key],kind)
    return result
