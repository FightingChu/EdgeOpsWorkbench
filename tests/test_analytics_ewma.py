import unittest
from edgeops.domain.analytics.ewma import smooth

class EwmaTests(unittest.TestCase):
    def test_smoothing_and_identity(self):
        self.assertEqual(smooth([2,6,10],.5), [2,4,7])
        self.assertEqual(smooth([2,6],1), [2,6])
    def test_invalid_alpha(self):
        with self.assertRaises(ValueError): smooth([1],0)
