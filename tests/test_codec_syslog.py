import unittest
from edgeops.codecs.syslog import decode

class SyslogTests(unittest.TestCase):
    def test_priority_and_structured_data(self):
        result=decode('<34>1 2026-10-21T00:00:00Z router api 3 ID7 [x a="b"] device failed')
        self.assertEqual(result['severity'],'critical'); self.assertEqual(result['message'],'device failed')
    def test_priority_outside_range(self):
        with self.assertRaises(ValueError): decode('<999>1 - host app - - - msg')
