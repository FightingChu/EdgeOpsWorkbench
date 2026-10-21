"""Export preserves the first cursor snapshot while later imports arrive."""
import json
from edgeops.application.exports import ExportService
from edgeops.codecs.ndjson import decode
from tests.support import IsolatedCase

class ExportSnapshotTests(IsolatedCase):
    def test_new_import_does_not_enter_later_export_pages(self):
        source=self.root/'events.jsonl'
        source.write_text(chr(10).join(json.dumps({'message':str(i),'severity':'info','recorded_at':'2026-10-21T00:00:00Z'}) for i in range(201)))
        self.operations.import_events(source)
        original=self.operations.list_events; calls=[]
        def injecting_query(query):
            page=original(query);calls.append(query)
            if len(calls)==1:
                path=self.root/'new.jsonl';path.write_text('{"message":"new","severity":"info","recorded_at":"2026-10-21T00:00:01Z"}')
                self.operations.import_events(path)
            return page
        self.operations.list_events=injecting_query
        target=self.root/'export.ndjson';ExportService(self.operations).export(target)
        records=decode(target.read_text())
        self.assertEqual(len(records),201)
        self.assertNotIn('new',[row['message'] for row in records])
