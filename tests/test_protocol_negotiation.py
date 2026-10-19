import unittest

from edgeops.devices.protocol import negotiate


class ProtocolNegotiationTests(unittest.TestCase):
    def test_highest_common_version_and_sorted_features(self):
        self.assertEqual(negotiate([1, 2], ["ack", "reading", "future"], supported_versions=(1, 2)), {"version": 2, "features": ["ack", "reading"]})

    def test_no_common_version_rejected(self):
        with self.assertRaisesRegex(ValueError, "compatible"):
            negotiate([9], [])
