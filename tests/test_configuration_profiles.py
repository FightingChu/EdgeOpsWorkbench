import unittest
from edgeops.configuration.profiles import select_profile

class ConfigProfileTests(unittest.TestCase):
    def test_named_profile_is_validated(self):
        document={'base':{'port':8877},'profiles':{'test':{'port':9000}}}
        self.assertEqual(select_profile(document,'test')['port'],9000)
    def test_unsafe_profile_rejected(self):
        with self.assertRaises(ValueError): select_profile({'base':{},'profiles':{'x':{'host':'0.0.0.0'}}},'x')
