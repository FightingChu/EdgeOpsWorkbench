import unittest
from edgeops.domain.alerting.engine import evaluate_rules

class AlertEngineTests(unittest.TestCase):
    def rule(self): return {'version':1,'id':'heat','condition':{'field':'value','op':'ge','value':85},'group_by':['device_id'],'severity':'critical'}
    def test_match_emits_stable_identity(self):
        event={'device_id':'a','value':90}
        self.assertEqual(evaluate_rules(event,[self.rule()]),evaluate_rules(event,[self.rule()]))
        self.assertEqual(evaluate_rules({'device_id':'a','value':80},[self.rule()]),[])
    def test_duplicate_rule_names_rejected(self):
        with self.assertRaises(ValueError): evaluate_rules({'device_id':'a','value':90},[self.rule(),self.rule()])
