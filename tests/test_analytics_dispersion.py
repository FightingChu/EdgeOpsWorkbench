import unittest
from edgeops.domain.analytics.dispersion import dispersion

class DispersionTests(unittest.TestCase):
    def test_population_and_sample(self):
        self.assertEqual(dispersion([1,3])['variance'], 1)
        self.assertEqual(dispersion([1,3], sample=True)['variance'], 2)
    def test_short_sample_rejected(self):
        with self.assertRaises(ValueError): dispersion([1], sample=True)
