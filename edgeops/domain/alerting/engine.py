"""Alert rule evaluation emits stable identities and explicit severities."""
from .validation import validate_rule
from .composite import evaluate_tree
from .fingerprint import identity

def evaluate_rules(record,rules):
    if not isinstance(rules,list) or len(rules)>1000: raise ValueError("too many rules")
    results=[]; seen=set()
    for rule in rules:
        validate_rule(rule)
        if rule['id'] in seen: raise ValueError("duplicate rule id")
        seen.add(rule['id'])
        if evaluate_tree(record,rule['condition']):
            results.append({'rule_id':rule['id'],'severity':rule['severity'],'fingerprint':identity(rule['id'],record,rule['group_by'])})
    return results
