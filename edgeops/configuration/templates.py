"""Configuration interpolation resolves only explicitly supplied scalar variables."""
from string import Template

def interpolate(value,variables,depth=0):
    if depth>20: raise ValueError("configuration template too deep")
    if not isinstance(variables,dict) or any(not isinstance(v,(str,int,float,bool)) for v in variables.values()): raise ValueError("variables must be scalar")
    if isinstance(value,dict): return {key:interpolate(item,variables,depth+1) for key,item in value.items()}
    if isinstance(value,list): return [interpolate(item,variables,depth+1) for item in value]
    if isinstance(value,str):
        try: return Template(value).substitute(variables)
        except (KeyError,ValueError): raise ValueError("unresolved configuration variable") from None
    return value
