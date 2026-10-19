from datetime import datetime, timezone
import unittest

from edgeops.domain import Device, TelemetryReading, evaluate_reading


class DomainTests(unittest.TestCase):
    def reading(self, metric, value):
        return TelemetryReading("device-1", metric, value, "unit", datetime.now(timezone.utc).isoformat())

    def test_device_rejects_control_characters(self):
        with self.assertRaisesRegex(ValueError, "printable"):
            Device("bad\nid", "Device", "sensor")

    def test_reading_requires_timezone(self):
        with self.assertRaisesRegex(ValueError, "timezone"):
            TelemetryReading("device-1", "temperature", 20, "C", "2026-10-19T10:00:00")

    def test_reading_rejects_non_finite_values(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            self.reading("temperature", float("nan"))

    def test_temperature_thresholds(self):
        self.assertIsNone(evaluate_reading(self.reading("temperature", 74.9)))
        self.assertEqual(evaluate_reading(self.reading("temperature", 75)).severity, "warning")
        self.assertEqual(evaluate_reading(self.reading("temperature", 85)).severity, "critical")

    def test_battery_thresholds_run_in_reverse(self):
        self.assertIsNone(evaluate_reading(self.reading("battery", 21)))
        self.assertEqual(evaluate_reading(self.reading("battery", 20)).severity, "warning")
        self.assertEqual(evaluate_reading(self.reading("battery", 10)).severity, "critical")


if __name__ == "__main__":
    unittest.main()

