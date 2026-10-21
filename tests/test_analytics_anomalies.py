import unittest
from edgeops.domain.analytics.anomalies import detect

class AnomalyTests(unittest.TestCase):
    def test_outlier_with_constant_baseline(self):
        self.assertEqual(detect([1,1,1,50])['indices'], [3])
        self.assertEqual(detect([1,1,1])['indices'], [])
    def test_threshold_bounds(self):
        with self.assertRaises(ValueError): detect([1],0)
