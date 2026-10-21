import unittest
from edgeops.codecs.registry import decode_events,formats

class CodecRegistryTests(unittest.TestCase):
    def test_dispatch_normalizes_events(self):
        self.assertEqual(decode_events('message=online severity=info','logfmt')[0]['message'],'online')
        self.assertIn('xml',formats())
    def test_unknown_format_rejected(self):
        with self.assertRaises(ValueError): decode_events('x','pickle')
