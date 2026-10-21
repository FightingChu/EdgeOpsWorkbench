"""Atomic object patch operations work on a copy and honor test preconditions."""
from copy import deepcopy
from .jsonpointer import tokens,lookup

def apply_patch(value,operations):
    if not isinstance(value,dict) or not isinstance(operations,list) or len(operations)>100: raise ValueError("invalid patch input")
    result=deepcopy(value)
    for operation in operations:
        if not isinstance(operation,dict) or operation.get('op') not in ('add','replace','remove','test'): raise ValueError("unknown patch operation")
        path=operation.get('path'); parts=tokens(path)
        if not parts: raise ValueError("root replacement is not permitted")
        target=lookup(result,'/'.join(path.split('/')[:-1])); key=parts[-1]
        if not isinstance(target,dict): raise ValueError("patch parent must be an object")
        op=operation['op']
        if op!='add' and key not in target: raise ValueError("patch target not found")
        if op=='test':
            if type(target[key]) is not type(operation.get('value')) or target[key]!=operation.get('value'): raise ValueError("patch test failed")
        elif op=='remove': del target[key]
        else:
            if 'value' not in operation: raise ValueError("patch value missing")
            target[key]=deepcopy(operation['value'])
    return result
