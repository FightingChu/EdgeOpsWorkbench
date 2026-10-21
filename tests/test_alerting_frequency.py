import unittest
from edgeops.domain.alerting.frequency import count_matches

class FrequencyTests(unittest.TestCase):
    def test_closed_window_and_stale_events(self):
        self.assertEqual(count_matches([0,5,10],10,5,2),{'count':2,'firing':True})
    def test_future_events_rejected(self):
        with self.assertRaises(ValueError): count_matches([11],10,5,1)
