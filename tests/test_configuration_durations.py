import unittest
from edgeops.configuration.durations import parse_duration

class DurationTests(unittest.TestCase):
    def test_units_and_fraction(self):
        self.assertEqual(parse_duration('250ms'),.25)
        self.assertEqual(parse_duration('1.5h'),5400)
    def test_bad_or_unbounded_duration(self):
        for value in ('0s','31d','10','-1s'):
            with self.assertRaises(ValueError): parse_duration(value)
