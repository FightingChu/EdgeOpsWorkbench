"""Deterministic destination selection deduplicates matching alert routes."""
from .composite import evaluate_tree

def destinations(record,routes):
    if not isinstance(routes,list) or len(routes)>100: raise ValueError("invalid routes")
    result=[]
    for route in routes:
        name=route.get('destination')
        if not isinstance(name,str) or not name or len(name)>128: raise ValueError("invalid destination")
        if evaluate_tree(record,route['when']) and name not in result: result.append(name)
    return result
