import unittest
from edgeops.configuration.patch import apply_patch

class ConfigPatchTests(unittest.TestCase):
    def test_test_and_replace_preserve_original(self):
        before={'api':{'port':1}}
        result=apply_patch(before,[{'op':'test','path':'/api/port','value':1},{'op':'replace','path':'/api/port','value':2}])
        self.assertEqual(result['api']['port'],2)
        self.assertEqual(before['api']['port'],1)
    def test_failed_precondition_is_atomic(self):
        before={'a':1}
        with self.assertRaises(ValueError): apply_patch(before,[{'op':'add','path':'/b','value':2},{'op':'test','path':'/a','value':9}])
        self.assertEqual(before,{'a':1})
