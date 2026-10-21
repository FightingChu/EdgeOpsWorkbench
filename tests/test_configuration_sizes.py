import unittest
from edgeops.configuration.sizes import parse_size

class ByteSizeTests(unittest.TestCase):
    def test_binary_and_decimal(self):
        self.assertEqual(parse_size('1KiB'),1024)
        self.assertEqual(parse_size('1KB'),1000)
    def test_invalid_sizes(self):
        for value in ('0B','2GiB','1mb'):
            with self.assertRaises(ValueError): parse_size(value)
