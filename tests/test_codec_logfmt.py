import unittest
from edgeops.codecs.logfmt import encode,decode

class LogfmtTests(unittest.TestCase):
    def test_quoted_spaces_equals_and_unicode(self):
        value={'message':'hello world=a','site':'北'}
        self.assertEqual(decode(encode(value)),value)
    def test_duplicate_key_rejected(self):
        with self.assertRaises(ValueError): decode('a=1 a=2')
