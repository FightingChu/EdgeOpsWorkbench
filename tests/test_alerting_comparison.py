import unittest
from edgeops.domain.alerting.comparison import compare

class ComparisonTests(unittest.TestCase):
    def test_explicit_types_and_boundaries(self):
        self.assertFalse(compare(True,'eq',1))
        self.assertTrue(compare(4,'ge',4))
        self.assertTrue(compare(1,'ne','1'))
    def test_unsafe_ordering_rejected(self):
        for actual in ('4',True,float('nan')):
            with self.assertRaises(ValueError): compare(actual,'gt',3)
