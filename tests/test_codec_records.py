import unittest
from edgeops.codecs.records import normalize

class CodecRecordTests(unittest.TestCase):
    def test_unknown_fields_preserved_in_metadata(self):
        result=normalize({'message':'热','severity':'WARNING','trace_id':'x'})
        self.assertEqual(result['metadata'],{'trace_id':'x'})
        self.assertEqual(result['severity'],'warning')
    def test_metadata_conflict_rejected(self):
        with self.assertRaises(ValueError): normalize({'message':'x','trace':1,'metadata':{'trace':2}})
