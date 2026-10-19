import unittest

from edgeops.devices.protocol import Frame, FrameParser, encode_frame


class ProtocolFramingTests(unittest.TestCase):
    def test_fragmented_frame_round_trips(self):
        raw = encode_frame(Frame(7, b"hello"))
        parser = FrameParser()
        frames = []
        for byte in raw:
            frames.extend(parser.feed(bytes([byte])))
        parser.finish()
        self.assertEqual(frames, [Frame(7, b"hello")])

    def test_checksum_length_version_and_truncation_rejected(self):
        raw = bytearray(encode_frame(Frame(1, b"x")))
        raw[-1] ^= 1
        with self.assertRaisesRegex(ValueError, "checksum"):
            FrameParser().feed(bytes(raw))
        with self.assertRaisesRegex(ValueError, "truncated"):
            parser = FrameParser(); parser.feed(encode_frame(Frame(1, b"x"))[:-1]); parser.finish()
        with self.assertRaisesRegex(ValueError, "magic"):
            FrameParser().feed(b"BAD!")
