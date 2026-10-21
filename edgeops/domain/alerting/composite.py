"""Nested all/any/not rules enforce depth and fan-out limits."""
from .predicate import evaluate

def evaluate_tree(record,tree,depth=0):
    if depth>8 or not isinstance(tree,dict): raise ValueError("invalid rule tree or depth")
    if 'field' in tree: return evaluate(record,tree)
    if len(tree)!=1: raise ValueError("composite requires exactly one operator")
    operator,children=next(iter(tree.items()))
    if operator=='not': return not evaluate_tree(record,children,depth+1)
    if operator not in ('all','any') or not isinstance(children,list) or not 1<=len(children)<=20:
        raise ValueError("invalid composite operator or children")
    results=[evaluate_tree(record,child,depth+1) for child in children]
    return all(results) if operator=='all' else any(results)
