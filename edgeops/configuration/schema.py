"""Configuration object validation preserves the repository's local-only contract."""
from pathlib import PureWindowsPath,PurePosixPath

def validate(values):
    if not isinstance(values,dict) or set(values)-{'host','port','data_dir','database_name'}: raise ValueError("unknown configuration fields")
    result={'host':'127.0.0.1','port':8877,'data_dir':'data','database_name':'edgeops.sqlite3',**values}
    if result['host'] not in ('127.0.0.1','localhost'): raise ValueError("host must be loopback")
    if type(result['port']) is not int or not 1<=result['port']<=65535: raise ValueError("invalid port")
    for name in ('data_dir','database_name'):
        if not isinstance(result[name],str) or not result[name].strip() or any(ord(c)<32 for c in result[name]): raise ValueError("invalid "+name)
    name=result['database_name']
    if PureWindowsPath(name).name!=name or PurePosixPath(name).name!=name or name in ('.','..') or ':' in name: raise ValueError("database_name must be a filename")
    return result
