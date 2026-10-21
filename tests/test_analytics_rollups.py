import unittest
from edgeops.domain.analytics.rollups import rollup

class RollupTests(unittest.TestCase):
    def test_groups_devices_and_metrics(self):
        rows=[{'device_id':'a','metric':'t','value':1},{'device_id':'a','metric':'t','value':3},{'device_id':'b','metric':'t','value':8}]
        self.assertEqual([r['mean'] for r in rollup(rows)],[2,8])
    def test_missing_identity_rejected(self):
        with self.assertRaises(ValueError): rollup([{'value':1}])
