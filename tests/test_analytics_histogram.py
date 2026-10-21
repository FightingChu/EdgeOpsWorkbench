import unittest
from edgeops.domain.analytics.histogram import histogram

class HistogramTests(unittest.TestCase):
    def test_right_endpoint_and_constant_data(self):
        self.assertEqual(histogram([0,1,2],2)['counts'], [1,2])
        self.assertEqual(histogram([1,1],2)['counts'], [2,0])
    def test_bins_rejected(self):
        with self.assertRaises(ValueError): histogram([1],0)
