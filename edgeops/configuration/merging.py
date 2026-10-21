"""Deep configuration overlays copy inputs and reject object/scalar conflicts."""
from copy import deepcopy

def merge_layers(*layers):
    result={}
    def apply(target,source,depth=0):
        if depth>20: raise ValueError("configuration nesting exceeds limit")
        for key,value in source.items():
            if not isinstance(key,str): raise ValueError("configuration keys must be text")
            if isinstance(value,dict):
                if key in target and not isinstance(target[key],dict): raise ValueError("configuration object conflicts with scalar")
                apply(target.setdefault(key,{}),value,depth+1)
            else: target[key]=deepcopy(value)
    for layer in layers:
        if not isinstance(layer,dict): raise ValueError("configuration layer must be an object")
        apply(result,layer)
    return result
