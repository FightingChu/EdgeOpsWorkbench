import unittest
from edgeops.codecs.keyvalue import encode,decode

class KeyValueTests(unittest.TestCase):
    def test_value_preserves_equals(self):
        self.assertEqual(decode(encode({'url':'x=y','site':'north'})),{'url':'x=y','site':'north'})
    def test_duplicate_and_newline_rejected(self):
        with self.assertRaises(ValueError): decode('a=1'+chr(10)+'a=2')
        with self.assertRaises(ValueError): encode({'a':'x'+chr(10)+'y'})
