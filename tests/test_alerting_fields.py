import unittest
from edgeops.domain.alerting.fields import field

class FieldTests(unittest.TestCase):
    def test_nested_field_and_missing_key(self):
        self.assertEqual(field({'meta':{'site':'north'}},'meta.site'),'north')
        with self.assertRaises(ValueError): field({'meta':None},'meta.site')
    def test_path_injection_rejected(self):
        with self.assertRaises(ValueError): field({},'meta[0]')
