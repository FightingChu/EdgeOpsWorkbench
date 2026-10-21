import unittest
from edgeops.domain.analytics.samples import numbers

class SamplesTests(unittest.TestCase):
    def test_values_and_generator(self):
        self.assertEqual(numbers(iter([1, 2])), [1.0, 2.0])
        self.assertEqual(numbers([], minimum=0), [])
    def test_empty_nonfinite_and_boolean(self):
        for values in ([], [True], [float('inf')], ['1']):
            with self.subTest(values=values), self.assertRaises(ValueError): numbers(values)
