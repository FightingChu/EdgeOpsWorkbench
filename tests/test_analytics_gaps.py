import unittest
from edgeops.domain.analytics.gaps import find_gaps

class GapTests(unittest.TestCase):
    def test_tolerance_and_gap_coordinates(self):
        self.assertEqual(find_gaps([0,10,31],10,1),[{'after':10,'before':31,'duration':21}])
    def test_unsorted_times_rejected(self):
        with self.assertRaises(ValueError): find_gaps([2,1],1)
