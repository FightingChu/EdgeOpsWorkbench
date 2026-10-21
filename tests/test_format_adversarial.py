"""Adversarial format inputs preserve bounds and reject ambiguous grammars."""
import unittest
from edgeops.configuration.durations import parse_duration
from edgeops.domain.deployment.artifacts import describe
from edgeops.domain.alerting.fields import field
from edgeops.codecs.gzipdata import encode,decode

class FormatAdversarialTests(unittest.TestCase):
    def test_separators_cannot_match_unescaped_regex_wildcards(self):
        with self.assertRaises(ValueError): parse_duration('1x5h')
        with self.assertRaises(ValueError): describe('fw','1x2x3',b'x')
        with self.assertRaises(ValueError): field({'a-b':1},'a-b')
    def test_compressed_limit_is_on_decoded_bytes(self):
        compressed=encode(b'x'*100000)
        self.assertLess(len(compressed),1000)
        with self.assertRaises(ValueError): decode(compressed,1000)
