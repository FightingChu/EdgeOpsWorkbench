"""Lossless dotted-key flattening rejects ambiguous nested key names."""

def flatten(values,prefix='',depth=0):
    if depth>20 or not isinstance(values,dict): raise ValueError("invalid object nesting")
    result={}
    for key,value in values.items():
        if not isinstance(key,str) or not key or '.' in key: raise ValueError("ambiguous configuration key")
        path=prefix+'.'+key if prefix else key
        if isinstance(value,dict) and value: result.update(flatten(value,path,depth+1))
        else: result[path]=value
    return result

def expand(values):
    result={}
    for path,value in values.items():
        if not isinstance(path,str) or not all(path.split('.')): raise ValueError("invalid flat path")
        parts=path.split('.'); target=result
        for key in parts[:-1]:
            if key in target and not isinstance(target[key],dict): raise ValueError("conflicting flat paths")
            target=target.setdefault(key,{})
        if parts[-1] in target: raise ValueError("conflicting flat paths")
        target[parts[-1]]=value
    return result
