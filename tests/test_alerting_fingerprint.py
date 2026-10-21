import unittest
from edgeops.domain.alerting.fingerprint import identity

class AlertIdentityTests(unittest.TestCase):
    def test_separator_collisions_do_not_merge_alerts(self):
        self.assertNotEqual(identity('r',{'a':'x:y','b':'z'},['a','b']),identity('r',{'a':'x','b':'y:z'},['a','b']))
    def test_missing_group_field_is_not_silently_empty(self):
        with self.assertRaises(ValueError): identity('r',{},['device_id'])
