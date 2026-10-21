import unittest
from edgeops.domain.deployment.inventory import normalize_devices

class DeploymentInventoryTests(unittest.TestCase):
    def device(self,name='a'): return {'id':name,'kind':'sensor','version':'1.0.0','online':True}
    def test_deterministic_inventory(self):
        self.assertEqual([x['id'] for x in normalize_devices([self.device('b'),self.device('a')])],['a','b'])
    def test_duplicate_target_rejected(self):
        with self.assertRaises(ValueError): normalize_devices([self.device(),self.device()])
