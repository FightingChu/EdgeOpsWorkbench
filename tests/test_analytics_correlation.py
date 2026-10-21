import unittest
from edgeops.domain.analytics.correlation import correlate

class CorrelationTests(unittest.TestCase):
    def test_positive_and_negative(self):
        self.assertAlmostEqual(correlate([1,2,3],[2,4,6]),1)
        self.assertAlmostEqual(correlate([1,2,3],[6,4,2]),-1)
    def test_constant_series_rejected(self):
        with self.assertRaises(ValueError): correlate([1,1],[1,2])
