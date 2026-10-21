import unittest
from edgeops.codecs.json_document import encode,decode

class JsonDocumentTests(unittest.TestCase):
    def test_round_trip_normalized_events(self):
        result=decode(encode([{'message':'中文','custom':2}]))
        self.assertEqual(result[0]['metadata'],{'custom':2})
    def test_duplicate_keys_and_nan(self):
        for text in ('[{"message":"a","message":"b"}]','[{"message":"a","x":NaN}]'):
            with self.assertRaises(ValueError): decode(text)
