import unittest
from edgeops.domain.alerting.severity import at_least

class SeverityTests(unittest.TestCase):
    def test_order_and_inclusive_minimum(self):
        self.assertTrue(at_least('error','warning'))
        self.assertTrue(at_least('warning','warning'))
        self.assertFalse(at_least('debug','info'))
    def test_unknown_level_rejected(self):
        with self.assertRaises(ValueError): at_least('fatal','info')
