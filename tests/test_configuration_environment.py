import unittest
from edgeops.configuration.environment import read_environment

class EnvironmentTests(unittest.TestCase):
    def test_allowlist_and_port_conversion(self):
        result=read_environment({'EDGEOPS_PORT':'9000','EDGEOPS_TOKEN':'secret'})
        self.assertEqual(result,{'port':9000})
    def test_invalid_numeric_setting(self):
        with self.assertRaises(ValueError): read_environment({'EDGEOPS_PORT':'one'})
