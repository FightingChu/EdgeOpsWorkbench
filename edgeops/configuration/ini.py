"""INI adapter enforces one explicit EdgeOps section and scalar types."""
import configparser
from .schema import validate
from .scalar import parse_scalar

def parse_ini(text):
    if not isinstance(text,str) or len(text)>65536: raise ValueError("invalid INI input size")
    parser=configparser.ConfigParser(interpolation=None,strict=True)
    try: parser.read_string(text)
    except configparser.Error as exc: raise ValueError("invalid INI: "+str(exc)) from None
    if parser.sections()!=['edgeops'] or parser.defaults(): raise ValueError("INI requires one edgeops section and no defaults")
    values=dict(parser['edgeops'])
    if 'port' in values: values['port']=parse_scalar(values['port'],'integer')
    return validate(values)
