import unittest
from edgeops.domain.analytics.topk import top_values

class TopValuesTests(unittest.TestCase):
    def test_ties_are_deterministic(self):
        self.assertEqual(top_values([{'s':'b'},{'s':'a'}],'s',1),[{'value':'a','count':1}])
    def test_wrong_type_rejected(self):
        with self.assertRaises(ValueError): top_values([{'s':1}],'s')
