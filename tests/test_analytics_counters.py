import unittest
from edgeops.domain.analytics.counters import counter_deltas

class CounterTests(unittest.TestCase):
    def test_reset_and_wrap(self):
        self.assertEqual(counter_deltas([5,8,2,4]), {'deltas':[3,2,2],'resets':1,'total':7})
        self.assertEqual(counter_deltas([254,1],256)['total'],3)
    def test_negative_counter_rejected(self):
        with self.assertRaises(ValueError): counter_deltas([-1,1])
