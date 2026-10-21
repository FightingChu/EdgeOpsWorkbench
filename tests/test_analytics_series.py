import unittest
from edgeops.domain.analytics.series import normalize

class SeriesTests(unittest.TestCase):
    def test_sort_and_identical_duplicate(self):
        self.assertEqual(normalize([(2,4),(1,3),(2,4)]),[{'time':1,'value':3},{'time':2,'value':4}])
    def test_conflicting_duplicate_rejected(self):
        with self.assertRaises(ValueError): normalize([(1,2),(1,3)])
