from datetime import datetime, timezone
import unittest

from edgeops.devices.protocol import Frame, decode_message, encode_frame
from edgeops.devices.protocol.messages import ReadingMessage, encode_message
from edgeops.domain import TelemetryReading


class ProtocolMessageTests(unittest.TestCase):
    def test_reading_message_round_trip(self):
        reading = TelemetryReading("press-01", "temperature", 70, "C", datetime(2026, 10, 19, tzinfo=timezone.utc).isoformat())
        frame = encode_message(ReadingMessage(reading, 8))
        message = decode_message(Frame(frame.message_type, frame.payload))
        self.assertEqual(message.sequence, 8)
        self.assertEqual(message.reading.value, 70)

    def test_extra_fields_and_wrong_type_rejected(self):
        with self.assertRaises(ValueError):
            decode_message(Frame(1, b'{"sequence":1,"device_id":"x","metric":"temperature","value":1,"unit":"C","recorded_at":"2026-10-19T00:00:00+00:00","x":1}'))
        with self.assertRaises(ValueError):
            decode_message(Frame(2, b"{}"))
