"""Evaluate operator rules against a fixed page of persisted event records."""
from ..domain.alerting.engine import evaluate_rules
from ..domain.event_query import EventQuery

class AlertingService:
    def __init__(self,operations): self.operations=operations
    def evaluate(self,rules,query=None):
        # Validate rules even when no events match the query.
        from ..domain.alerting.validation import validate_rule
        if not isinstance(rules,list) or len(rules)>1000: raise ValueError('invalid rule set')
        identities=set()
        for rule in rules:
            validate_rule(rule)
            if rule['id'] in identities: raise ValueError('duplicate rule id')
            identities.add(rule['id'])
        page=self.operations.list_events(query or EventQuery())
        results=[]
        for event in page['events']:
            for match in evaluate_rules(event,rules): results.append({'event_id':event['id'],**match})
        return {'evaluated_events':len(page['events']),'matches':results,'next_cursor':page['next_cursor'],'snapshot_id':page['snapshot_id']}
