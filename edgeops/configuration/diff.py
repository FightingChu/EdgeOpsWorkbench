"""Configuration differences report changed leaves with precise dotted keys."""
from copy import deepcopy

def changes(before,after,prefix=''):
    if not isinstance(before,dict) or not isinstance(after,dict): raise ValueError("diff inputs must be objects")
    result=[]
    for key in sorted(set(before)|set(after)):
        path=prefix+'.'+key if prefix else key
        if key not in before: result.append({'path':path,'op':'add','value':deepcopy(after[key])})
        elif key not in after: result.append({'path':path,'op':'remove','old':deepcopy(before[key])})
        elif isinstance(before[key],dict) and isinstance(after[key],dict): result.extend(changes(before[key],after[key],path))
        elif type(before[key]) is not type(after[key]) or before[key]!=after[key]: result.append({'path':path,'op':'replace','old':deepcopy(before[key]),'value':deepcopy(after[key])})
    return result
