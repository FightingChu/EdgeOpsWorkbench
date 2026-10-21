import unittest
from edgeops.configuration.templates import interpolate

class TemplateTests(unittest.TestCase):
    def test_explicit_variables_and_literal_dollar(self):
        self.assertEqual(interpolate({'name':'$SITE $$'},{'SITE':'north'}),{'name':'north $'})
    def test_missing_variable_does_not_read_environment(self):
        with self.assertRaises(ValueError): interpolate('$HOME',{})
