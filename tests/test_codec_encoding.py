import unittest
from edgeops.codecs.encoding import decode

class TextEncodingTests(unittest.TestCase):
    def test_bom_and_explicit_chinese_encoding(self):
        self.assertEqual(decode('中文'.encode('gb18030'),'gb18030'),'中文')
        self.assertEqual(decode(bytes([239,187,191,120]),'utf-8-sig'),'x')
    def test_invalid_bytes_not_replaced(self):
        with self.assertRaises(ValueError): decode(bytes([255]),'utf-8')
