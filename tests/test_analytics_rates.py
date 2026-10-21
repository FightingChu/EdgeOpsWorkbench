import unittest
from edgeops.domain.analytics.rates import rates

class RateTests(unittest.TestCase):
    def test_irregular_intervals(self):
        self.assertEqual(rates([0,2,5],[0,4,13]),[2,3])
    def test_repeated_time_rejected(self):
        with self.assertRaises(ValueError): rates([1,1],[1,2])
