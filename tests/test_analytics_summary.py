import unittest
from edgeops.domain.analytics.summary import summarize

class SummaryTests(unittest.TestCase):
    def test_summary_integrates_statistics(self):
        result=summarize([1,2,3])
        self.assertEqual((result['count'],result['mean'],result['p50']),(3,2,2))
        self.assertIn('variance',result['dispersion'])
    def test_no_synthetic_empty_values(self):
        with self.assertRaises(ValueError): summarize([])
