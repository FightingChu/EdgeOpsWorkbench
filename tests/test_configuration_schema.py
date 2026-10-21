import unittest
from edgeops.configuration.schema import validate

class ConfigSchemaTests(unittest.TestCase):
    def test_defaults_and_override(self):
        self.assertEqual(validate({'port':9000})['host'],'127.0.0.1')
    def test_external_host_bool_port_and_path_rejected(self):
        for value in ({'host':'0.0.0.0'},{'port':True},{'database_name':'../x'},{'database_name':'C:db'}):
            with self.assertRaises(ValueError): validate(value)
