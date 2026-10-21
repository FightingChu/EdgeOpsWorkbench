import unittest
from edgeops.codecs.content_types import resolve

class ContentTypeTests(unittest.TestCase):
    def test_case_and_charset(self):
        self.assertEqual(resolve('Application/JSON; charset=utf-8'),'json')
    def test_unsupported_type_or_charset(self):
        for value in ('text/html','application/json; charset=latin1'):
            with self.assertRaises(ValueError): resolve(value)
