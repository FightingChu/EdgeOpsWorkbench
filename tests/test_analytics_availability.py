import unittest
from edgeops.domain.analytics.availability import availability

class AvailabilityTests(unittest.TestCase):
    def test_overlapping_outages_are_not_double_counted(self):
        self.assertEqual(availability(0,10,[(-1,2),(1,4),(8,20)])['downtime'],6)
    def test_reversed_window_rejected(self):
        with self.assertRaises(ValueError): availability(10,0,[])
