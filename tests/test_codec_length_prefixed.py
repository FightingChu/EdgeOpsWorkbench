import unittest
from edgeops.codecs.length_prefixed import encode,Decoder

class LengthPrefixTests(unittest.TestCase):
    def test_fragmented_records_include_empty_record(self):
        parser=Decoder(); output=[]
        for byte in encode([b'',b'abc']): output.extend(parser.feed(bytes([byte])))
        parser.finish(); self.assertEqual(output,[b'',b'abc'])
    def test_truncated_record_rejected(self):
        parser=Decoder(); parser.feed(encode([b'x'])[:-1])
        with self.assertRaises(ValueError): parser.finish()
