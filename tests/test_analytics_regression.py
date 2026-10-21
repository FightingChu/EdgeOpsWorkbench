import unittest
from edgeops.domain.analytics.regression import fit

class RegressionTests(unittest.TestCase):
    def test_recovers_line(self):
        self.assertEqual(fit([0,1,2],[1,3,5]), {'slope':2,'intercept':1})
    def test_constant_or_mismatched_inputs(self):
        with self.assertRaises(ValueError): fit([1,1],[2,3])
        with self.assertRaises(ValueError): fit([0,1],[1,2,3])
