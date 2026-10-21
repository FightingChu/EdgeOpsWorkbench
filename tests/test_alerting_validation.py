import unittest
from edgeops.domain.alerting.validation import validate_rule

class RuleValidationTests(unittest.TestCase):
    def rule(self): return {'version':1,'id':'heat','condition':{'field':'value','op':'gt','value':85},'group_by':['device_id'],'severity':'error'}
    def test_supported_contract(self):
        self.assertEqual(validate_rule(self.rule())['id'],'heat')
    def test_version_and_group_bounds(self):
        for patch in ({'version':2},{'group_by':['x']*9}):
            with self.assertRaises(ValueError): validate_rule({**self.rule(),**patch})
