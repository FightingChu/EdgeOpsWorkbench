"""Event conversion retains Unicode and prevents destination overwrite."""
from edgeops.application.interchange import InterchangeService
from edgeops.codecs.csv_events import decode
from tests.support import IsolatedCase

class InterchangeServiceTests(IsolatedCase):
    def test_json_to_csv_preserves_normalized_metadata(self):
        source=self.root/'source.json';source.write_text('[{"message":"海鸥","trace":7}]',encoding='utf-8')
        target=self.root/'target.csv';result=InterchangeService().convert(source,target,'json','csv')
        self.assertEqual(result['records'],1)
        self.assertEqual(decode(target.read_text(encoding='utf-8'))[0]['metadata'],{'trace':7})
        with self.assertRaises(ValueError): InterchangeService().convert(source,target,'json','csv')
    def test_invalid_source_does_not_create_destination(self):
        source=self.root/'broken.json';source.write_text('[')
        target=self.root/'result.csv'
        with self.assertRaises(ValueError): InterchangeService().convert(source,target,'json','csv')
        self.assertFalse(target.exists())
