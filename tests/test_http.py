from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

from edgeops.api import make_server
from edgeops.application import OperationsService
from edgeops.config import Settings
from edgeops.devices import load_demo


class HttpTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        data_dir = Path(self.temporary.name)
        settings = Settings(host="127.0.0.1", port=0, data_dir=data_dir)
        load_demo(OperationsService(settings.database_path), datetime(2026, 10, 19, tzinfo=timezone.utc))
        self.server = make_server(settings)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)
        self.temporary.cleanup()

    def get_json(self, path):
        with urlopen(self.base + path, timeout=5) as response:
            return response.status, json.loads(response.read())

    def test_health_and_summary(self):
        status, health = self.get_json("/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(health["status"], "ok")
        _, summary = self.get_json("/api/summary")
        self.assertEqual(summary["devices"], 3)
        self.assertEqual(summary["open_incidents"], 4)

    def test_dashboard_is_served(self):
        with urlopen(self.base + "/", timeout=5) as response:
            body = response.read().decode("utf-8")
        self.assertIn("EdgeOps Workbench", body)
        self.assertIn("/app.js", body)

    def test_telemetry_limit_is_validated(self):
        with self.assertRaises(HTTPError) as caught:
            urlopen(self.base + "/api/telemetry?limit=999", timeout=5)
        self.assertEqual(caught.exception.code, 400)


if __name__ == "__main__":
    unittest.main()

