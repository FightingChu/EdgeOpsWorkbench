import unittest
from edgeops.codecs.gzipdata import encode,decode

class GzipTests(unittest.TestCase):
    def test_roundtrip_and_deterministic_header(self):
        self.assertEqual(decode(encode(b'hello')),b'hello')
        self.assertEqual(encode(b'hello'),encode(b'hello'))
    def test_bomb_truncation_and_concatenation(self):
        for data,limit in ((encode(b'x'*1000),10),(encode(b'x')[:-1],100),(encode(b'x')+encode(b'y'),100)):
            with self.assertRaises(ValueError): decode(data,limit)
