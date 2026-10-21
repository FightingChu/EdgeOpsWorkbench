import unittest
from edgeops.domain.alerting.textmatch import match_text

class TextMatchTests(unittest.TestCase):
    def test_casefold_and_literal_metacharacters(self):
        self.assertTrue(match_text('Straße','contains','STRASSE',False))
        self.assertFalse(match_text('aaa','contains','a.*'))
    def test_bounded_pattern(self):
        with self.assertRaises(ValueError): match_text('x','contains','x'*257)
