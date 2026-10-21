import unittest
from edgeops.configuration.ini import parse_ini

class IniTests(unittest.TestCase):
    def test_port_and_literal_percent(self):
        self.assertEqual(parse_ini('[edgeops]\nport=9000\ndata_dir=100%data')['data_dir'],'100%data')
    def test_duplicate_keys_rejected(self):
        with self.assertRaises(ValueError): parse_ini('[edgeops]\nport=1\nport=2')
