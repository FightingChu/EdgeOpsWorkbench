import unittest
from edgeops.codecs.checksummed import encode,decode

class EnvelopeTests(unittest.TestCase):
    def test_empty_and_nonempty_roundtrip(self):
        self.assertEqual(decode(encode(b'')),b'')
        self.assertEqual(decode(encode(b'abc')),b'abc')
    def test_tampering_and_truncation_rejected(self):
        with self.assertRaises(ValueError): decode(encode(b'abc')[:-1])
        with self.assertRaises(ValueError): decode(encode(b'abc')[:-1]+b'z')
