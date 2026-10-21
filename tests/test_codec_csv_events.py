import unittest
from edgeops.codecs.csv_events import encode,decode

class CsvEventTests(unittest.TestCase):
    def test_quoted_newline_and_metadata_roundtrip(self):
        message='line one'+chr(10)+'line, two'
        row=decode(encode([{'message':message,'metadata':{'x':'值'}}]))[0]
        self.assertEqual(row['message'],message)
        self.assertEqual(row['metadata'],{'x':'值'})
    def test_wrong_header_rejected(self):
        with self.assertRaises(ValueError): decode('unexpected,columns')
