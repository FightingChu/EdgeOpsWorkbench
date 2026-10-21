import unittest
from edgeops.domain.alerting.silence import is_silenced

class SilenceTests(unittest.TestCase):
    def test_scope_and_end_boundary(self):
        windows=[{'start':10,'end':20,'device_id':'a'}]
        self.assertTrue(is_silenced('r','a',10,windows))
        self.assertFalse(is_silenced('r','a',20,windows))
        self.assertFalse(is_silenced('r','b',15,windows))
    def test_reversed_window_rejected(self):
        with self.assertRaises(ValueError): is_silenced('r','a',5,[{'start':10,'end':9}])
