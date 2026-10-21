import unittest
from edgeops.codecs.ndjson import encode,decode

class NdjsonTests(unittest.TestCase):
    def test_blank_lines_and_roundtrip(self):
        self.assertEqual(decode(chr(10)+encode([{'message':'x'}]))[0]['message'],'x')
    def test_invalid_tail_rejects_document(self):
        with self.assertRaisesRegex(ValueError,'line 2'): decode('{"message":"x"}'+chr(10)+'{')
