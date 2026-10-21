"""A grouped severity rule can be routed, muted, and cooldown-limited deterministically."""
import unittest
from edgeops.domain.alerting.engine import evaluate_rules
from edgeops.domain.alerting.routing import destinations
from edgeops.domain.alerting.cooldown import eligible
from edgeops.domain.alerting.silence import is_silenced

class AlertRuleIntegrationTests(unittest.TestCase):
    def test_rule_to_notification_policy_chain(self):
        record={'device_id':'press','severity':'error','message':'hot'}
        condition={'field':'severity','op':'severity','value':'warning'}
        rules=[{'version':1,'id':'severity','condition':condition,'group_by':['device_id'],'severity':'critical'}]
        matches=evaluate_rules(record,rules)
        self.assertEqual(len(matches),1)
        self.assertEqual(destinations(record,[{'destination':'ops','when':condition}]),['ops'])
        self.assertFalse(eligible(10,8,5))
        self.assertTrue(is_silenced('severity','press',10,[{'start':9,'end':11,'rule_id':'severity'}]))
