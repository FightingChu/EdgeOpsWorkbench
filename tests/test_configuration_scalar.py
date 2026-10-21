import unittest
from edgeops.configuration.scalar import parse_scalar

class ConfigScalarTests(unittest.TestCase):
    def test_explicit_boolean_and_integer(self):
        self.assertFalse(parse_scalar('false','boolean'))
        self.assertEqual(parse_scalar('-12','integer'),-12)
    def test_no_coercion_of_bool_or_nonfinite(self):
        for value,kind in ((True,'integer'),('NaN','number'),('yes','boolean')):
            with self.assertRaises(ValueError): parse_scalar(value,kind)
