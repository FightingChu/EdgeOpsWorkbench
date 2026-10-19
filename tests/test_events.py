import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from edgeops.application import OperationsService
from edgeops.domain.event_query import EventQuery
from edgeops.application.event_import import MAX_FILE_BYTES, MAX_RECORDS, parse_event_file


class EventTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.service = OperationsService(self.root / "db.sqlite3")

    def tearDown(self):
        self.tmp.cleanup()

    def source(self, records, name="events.jsonl"):
        path = self.root / name
        path.write_text("\n".join(json.dumps(record, ensure_ascii=False) for record in records), encoding="utf-8")
        return path

    def event(self, index=0, **overrides):
        return {"message": f"record {index}", "severity": "info", "service": "api",
                "recorded_at": "2026-10-19T09:00:00Z", **overrides}

    def test_reimport_and_copied_source_retain_origins(self):
        records = [self.event(), self.event(), self.event(1)]
        first = self.service.import_events(self.source(records))
        second = self.service.import_events(self.source(records, "copy.jsonl"))
        self.assertEqual((first["inserted_count"], first["duplicate_count"]), (2, 1))
        self.assertEqual((second["inserted_count"], second["duplicate_count"]), (0, 3))
        with self.service.database.connect() as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM event_origins").fetchone()[0], 6)

    def test_coordinates_use_physical_lines_and_encoded_bytes(self):
        path = self.root / "coords.txt"
        path.write_bytes("\r\n海鸥\r\n\nlast".encode("utf-8"))
        self.service.import_events(path, format="text")
        rows = self.service.list_events()["events"]
        self.assertEqual([(row["physical_line"], row["byte_offset"]) for row in rows], [(4, 11), (2, 2)])
        self.assertIsNone(rows[0]["recorded_at"])

    def test_malformed_tail_commits_nothing(self):
        self.service.initialize()
        path = self.source([self.event()])
        with path.open("ab") as stream:
            stream.write(b'\n{"message":')
        with self.assertRaisesRegex(ValueError, "line 2"):
            self.service.import_events(path)
        self.assertEqual(self.service.list_events()["events"], [])
        with self.service.database.connect() as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM event_imports").fetchone()[0], 0)

    def test_storage_failure_rolls_back_audit_events_and_origins(self):
        self.service.initialize()
        with self.service.database.connect() as connection:
            connection.execute("""CREATE TRIGGER reject_second BEFORE INSERT ON events
                                WHEN NEW.message='record 1' BEGIN SELECT RAISE(ABORT,'injected'); END""")
        with self.assertRaises(sqlite3.IntegrityError):
            self.service.import_events(self.source([self.event(), self.event(1)]))
        with self.service.database.connect() as connection:
            for table in ("events", "event_origins", "event_imports"):
                self.assertEqual(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0], 0)

    def test_equivalent_timezone_and_json_order_deduplicate(self):
        self.service.import_events(self.source([
            self.event(recorded_at="2026-10-19T17:00:00+08:00", labels={"b": 2, "a": 1}),
            self.event(recorded_at="2026-10-19T09:00:00Z", labels={"a": 1, "b": 2}),
        ]))
        rows = self.service.list_events()["events"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["metadata"], {"labels": {"a": 1, "b": 2}})

    def test_pages_remain_stable_during_import(self):
        self.service.import_events(self.source([self.event(i) for i in range(9)]))
        page = self.service.list_events(EventQuery(limit=3))
        ids = [row["id"] for row in page["events"]]
        self.service.import_events(self.source([self.event(99)], "new.jsonl"))
        while page["next_cursor"]:
            page = self.service.list_events(EventQuery(limit=3, cursor=page["next_cursor"]))
            ids += [row["id"] for row in page["events"]]
        self.assertEqual(ids, list(range(9, 0, -1)))
        self.assertEqual(len(set(ids)), 9)

    def test_cursor_rejects_changed_filters(self):
        self.service.import_events(self.source([self.event(i) for i in range(3)]))
        cursor = self.service.list_events(EventQuery(limit=1))["next_cursor"]
        with self.assertRaisesRegex(ValueError, "cursor"):
            EventQuery(cursor=cursor, severity="error")

    def test_literal_search_and_combined_time_filters(self):
        self.service.import_events(self.source([
            self.event(0, message="100%_\\ done", device_id="unknown", severity="error"),
            self.event(1, message="100xxy done", severity="error"),
            self.event(2, message="100%_\\ done", recorded_at="2026-10-19T09:00:01Z"),
        ]))
        query = EventQuery(q="%_\\", device_id="unknown", service="api", severity="error",
                           since="2026-10-19T17:00:00+08:00", until="2026-10-19T09:00:00Z")
        rows = self.service.list_events(query)["events"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["device_id"], "unknown")

    def test_limits_cover_bytes_records_and_whole_file(self):
        path = self.root / "large.txt"
        path.write_bytes(b"x" * 65537)
        with self.assertRaisesRegex(ValueError, "65536"):
            parse_event_file(path, format="text")
        path.write_bytes(b"one\ntwo\n")
        with patch("edgeops.application.event_import.MAX_RECORDS", 1):
            with self.assertRaisesRegex(ValueError, "records"):
                parse_event_file(path, format="text")
        with patch("edgeops.application.event_import.MAX_FILE_BYTES", 5):
            with self.assertRaisesRegex(ValueError, "bytes"):
                parse_event_file(path, format="text")
        self.assertEqual((MAX_FILE_BYTES, MAX_RECORDS), (8388608, 10000))

    def test_invalid_encoding_and_duplicate_keys_rejected(self):
        for data in (b'\xff', b'{"message":"a","message":"b"}', b'{"x":NaN}', b'[]'):
            with self.subTest(data=data):
                path = self.root / "bad.jsonl"
                path.write_bytes(data)
                with self.assertRaises(ValueError):
                    self.service.import_events(path)

    def test_explicit_legacy_encoding(self):
        path = self.root / "legacy.log"
        path.write_bytes("设备离线".encode("gb18030"))
        self.service.import_events(path, format="text", encoding="gb18030")
        self.assertEqual(self.service.list_events()["events"][0]["message"], "设备离线")

    def test_filters_bound_high_cardinality(self):
        self.service.import_events(self.source([self.event(i, service=f"svc-{i:03}") for i in range(205)]))
        filters = self.service.event_filters()
        self.assertEqual(len(filters["services"]), 200)
        self.assertTrue(filters["truncated"]["services"])


if __name__ == "__main__":
    unittest.main()
