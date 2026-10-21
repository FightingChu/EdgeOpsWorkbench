import unittest
from edgeops.domain.alerting.consecutive import advance

class ConsecutiveTests(unittest.TestCase):
    def test_reset_and_saturation(self):
        self.assertEqual(advance(2,False,3),{'count':0,'firing':False})
        self.assertEqual(advance(3,True,3),{'count':3,'firing':True})
    def test_invalid_count_rejected(self):
        with self.assertRaises(ValueError): advance(-1,True,3)
