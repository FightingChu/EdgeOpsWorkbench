"""Database export spans pages under one insertion snapshot."""
import json
from edgeops.application.exports import ExportService
from edgeops.codecs.ndjson import decode
from tests.support import IsolatedCase

class EventExportServiceTests(IsolatedCase):
    def test_multi_page_export_has_no_duplicate_records(self):
        source=self.root/'events.jsonl'
        source.write_text(chr(10).join(json.dumps({'message':str(i),'severity':'info','recorded_at':'2026-10-21T00:00:00Z'}) for i in range(205)))
        self.operations.import_events(source)
        target=self.root/'events.ndjson';result=ExportService(self.operations).export(target)
        self.assertEqual(result['records'],205)
        self.assertEqual(len({row['message'] for row in decode(target.read_text())}),205)
    def test_limit_is_explicit_and_existing_output_is_untouched(self):
        target=self.root/'protected.json';target.write_text('keep')
        with self.assertRaises(ValueError): ExportService(self.operations).export(target)
        self.assertEqual(target.read_text(),'keep')
