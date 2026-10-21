import unittest
from edgeops.domain.analytics.quantiles import percentile

class QuantileTests(unittest.TestCase):
    def test_interpolation_and_endpoints(self):
        self.assertEqual(percentile([10, 0, 20, 30], 25), 7.5)
        self.assertEqual(percentile([7], 99), 7)
    def test_percent_bounds(self):
        for percent in (-1, 101, True):
            with self.assertRaises(ValueError): percentile([1], percent)
