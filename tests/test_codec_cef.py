import unittest
from edgeops.codecs.cef import decode

class CefTests(unittest.TestCase):
    def test_escaped_pipe_in_event_name(self):
        value='CEF:0|Acme|Sensor|1|100|heat'+chr(92)+'|warning|8|src=127.0.0.1'
        self.assertEqual(decode(value)['name'],'heat|warning')
    def test_bad_severity_rejected(self):
        with self.assertRaises(ValueError): decode('CEF:0|A|B|1|id|name|11|')
