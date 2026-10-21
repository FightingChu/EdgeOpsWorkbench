import unittest
from edgeops.domain.alerting.cooldown import eligible

class CooldownTests(unittest.TestCase):
    def test_boundary_and_first_notification(self):
        self.assertTrue(eligible(10,None,5))
        self.assertFalse(eligible(14,10,5))
        self.assertTrue(eligible(15,10,5))
    def test_clock_reversal_rejected(self):
        with self.assertRaises(ValueError): eligible(9,10,5)
