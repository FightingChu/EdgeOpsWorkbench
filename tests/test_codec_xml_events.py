import unittest
from edgeops.codecs.xml_events import decode

class XmlEventTests(unittest.TestCase):
    def test_unicode_and_escaped_message(self):
        self.assertEqual(decode('<events><event><message>热 &amp; cold</message></event></events>')[0]['message'],'热 & cold')
    def test_entities_and_duplicate_fields_rejected(self):
        for value in ('<!DOCTYPE x><events/>','<events><event><message>a</message><message>b</message></event></events>'):
            with self.assertRaises(ValueError): decode(value)
