import unittest
from edgeops.domain.analytics.windows import bucket

class WindowTests(unittest.TestCase):
    def test_bucket_edges_and_negative_time(self):
        self.assertEqual([x['start'] for x in bucket([-1,0,10],[2,4,6],10)],[-10,0,10])
    def test_zero_width_rejected(self):
        with self.assertRaises(ValueError): bucket([0],[1],0)
