import unittest
from edgeops.domain.analytics.moving import moving_average

class MovingTests(unittest.TestCase):
    def test_warmup_and_partial(self):
        self.assertEqual(moving_average([1,3,5],2), [None,2,4])
        self.assertEqual(moving_average([1,3,5],2,True), [1,2,4])
    def test_window_bounds(self):
        with self.assertRaises(ValueError): moving_average([1],0)
