from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from edgeops.api import make_server
from edgeops.application import OperationsService
from edgeops.config import Settings
from edgeops.devices import load_demo


class EventHttpTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        root = Path(self.temporary.name)
        self.source = root / "events.jsonl"
        self.source.write_text('{"message":"http event","severity":"warning","recorded_at":"2026-10-19T09:00:00Z"}\n', encoding="utf-8")
        settings = Settings(host="127.0.0.1", port=0, data_dir=root)
        self.service = OperationsService(settings.database_path)
        load_demo(self.service, datetime(2026, 10, 19, tzinfo=timezone.utc))
        self.service.import_events(self.source)
        self.server = make_server(settings)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join(timeout=3); self.temporary.cleanup()

    def get(self, path, host=None):
        request = Request(self.base + path, headers={"Host": host or self.base.removeprefix("http://")})
        with urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read())

    def test_event_page_filters_and_manifest_are_served(self):
        status, body = self.get("/api/events?severity=warning&limit=1")
        self.assertEqual(status, 200)
        self.assertEqual(body["events"][0]["message"], "http event")
        status, filters = self.get("/api/events/filters")
        self.assertEqual(status, 200)
        self.assertIn("warning", filters["severities"])
        with urlopen(self.base + "/manifest.webmanifest", timeout=5) as response:
            self.assertIn("EdgeOps", response.read().decode("utf-8"))

    def test_untrusted_host_is_rejected(self):
        with self.assertRaises(HTTPError) as caught:
            self.get("/api/events", host="127.0.0.2:" + self.base.rsplit(":", 1)[1])
        self.assertEqual(caught.exception.code, 403)

