"""Persisted event evaluation produces real identities and preserves pagination."""
import json
from edgeops.application.alerting import AlertingService
from edgeops.domain.event_query import EventQuery
from tests.support import IsolatedCase

class AlertingServiceTests(IsolatedCase):
    def rule(self): return {'version':1,'id':'errors','condition':{'field':'severity','op':'severity','value':'error'},'group_by':['device_id'],'severity':'critical'}
    def test_rules_against_database_snapshot(self):
        path=self.root/'events.jsonl'
        rows=[{'message':'online','severity':'info','device_id':'a','recorded_at':'2026-10-21T00:00:00Z'},{'message':'failed','severity':'error','device_id':'a','recorded_at':'2026-10-21T00:00:01Z'}]
        path.write_text(chr(10).join(json.dumps(row) for row in rows),encoding='utf-8');self.operations.import_events(path)
        result=AlertingService(self.operations).evaluate([self.rule()],EventQuery(limit=1))
        self.assertEqual(result['evaluated_events'],1);self.assertEqual(len(result['matches']),1)
        self.assertIsNotNone(result['next_cursor'])
    def test_invalid_rules_rejected_for_empty_database(self):
        with self.assertRaises(ValueError): AlertingService(self.operations).evaluate([{'version':99}])
