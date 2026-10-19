from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest

from edgeops.application import OperationsService
from edgeops.devices import load_demo
from edgeops.domain import TelemetryReading


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.database = Path(self.temporary.name) / "edgeops.sqlite3"
        self.service = OperationsService(self.database)

    def tearDown(self):
        self.temporary.cleanup()

    def test_demo_creates_devices_readings_and_incidents(self):
        summary = load_demo(self.service, datetime(2026, 10, 19, tzinfo=timezone.utc))
        self.assertEqual(summary, {
            "devices": 3,
            "telemetry": 5,
            "open_incidents": 4,
            "critical_incidents": 1,
        })
        self.assertEqual(len(self.service.list_devices()), 3)
        self.assertEqual(len(self.service.list_incidents()), 4)
        self.assertEqual(len(self.service.recent_telemetry()), 5)

    def test_repeated_threshold_updates_incident_occurrences(self):
        start = datetime(2026, 10, 19, tzinfo=timezone.utc)
        load_demo(self.service, start)
        load_demo(self.service, start)
        incidents = self.service.list_incidents()
        self.assertEqual(len(incidents), 4)
        self.assertTrue(all(item["occurrences"] == 2 for item in incidents))
        self.assertEqual(self.service.summary()["telemetry"], 10)

    def test_unknown_device_does_not_create_a_reading(self):
        reading = TelemetryReading(
            "missing", "temperature", 90, "C", datetime.now(timezone.utc).isoformat()
        )
        with self.assertRaisesRegex(ValueError, "not registered"):
            self.service.ingest(reading)
        self.assertEqual(self.service.summary()["telemetry"], 0)

    def test_recent_telemetry_limit_is_bounded(self):
        self.service.initialize()
        with self.assertRaisesRegex(ValueError, "between 1 and 200"):
            self.service.recent_telemetry(0)
        with self.assertRaisesRegex(ValueError, "between 1 and 200"):
            self.service.recent_telemetry(201)


if __name__ == "__main__":
    unittest.main()

