import unittest
from dataclasses import asdict
from edgeops.domain.deployment.artifacts import describe
from edgeops.domain.deployment.planning import plan
from edgeops.domain.deployment.policy import RolloutPolicy

class RolloutPlanTests(unittest.TestCase):
    def test_canary_waves_and_offline_device(self):
        devices=[{'id':str(i),'kind':'sensor','version':'1.0.0','online':i!=3} for i in range(4)]
        manifest={'version':1,'artifact':asdict(describe('fw','2.0.0',b'x')),'device_kind':'sensor','minimum_version':'1.0.0'}
        result=plan(devices,manifest,RolloutPolicy(batch_size=2))
        self.assertEqual(result['waves'],[['0'],['1','2']]); self.assertEqual(result['blocked'][0]['device_id'],'3')
    def test_invalid_inventory_is_not_ignored(self):
        with self.assertRaises(ValueError): plan([],{},RolloutPolicy())
