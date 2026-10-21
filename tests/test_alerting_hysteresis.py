import unittest
from edgeops.domain.alerting.hysteresis import active

class HysteresisTests(unittest.TestCase):
    def test_alert_stays_active_until_recovery(self):
        self.assertTrue(active(85,85,75))
        self.assertTrue(active(80,85,75,True))
        self.assertFalse(active(75,85,75,True))
    def test_invalid_threshold_order(self):
        with self.assertRaises(ValueError): active(80,75,85)
