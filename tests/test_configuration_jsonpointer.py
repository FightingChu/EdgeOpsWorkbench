import unittest
from edgeops.configuration.jsonpointer import lookup,tokens

class JsonPointerTests(unittest.TestCase):
    def test_escaped_tokens_and_root(self):
        value={'a/b':{'~x':3}}
        self.assertEqual(lookup(value,'/a~1b/~0x'),3)
        self.assertEqual(lookup(value,''),value)
    def test_invalid_escape_rejected(self):
        with self.assertRaises(ValueError): tokens('/bad~3')
