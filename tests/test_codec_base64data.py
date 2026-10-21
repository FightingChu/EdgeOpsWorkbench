import unittest
from edgeops.codecs.base64data import encode,decode

class Base64Tests(unittest.TestCase):
    def test_binary_roundtrip(self):
        self.assertEqual(decode(encode(bytes(range(256)))),bytes(range(256)))
    def test_whitespace_and_size_rejected(self):
        with self.assertRaises(ValueError): decode('YQ== '+chr(10))
        with self.assertRaises(ValueError): decode('YWJj',2)
