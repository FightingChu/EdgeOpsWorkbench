import unittest
from edgeops.domain.deployment.artifacts import describe
from edgeops.domain.deployment.simulator import simulate

class FirmwareSimulatorTests(unittest.TestCase):
    def test_success_requires_verified_bytes(self):
        artifact=describe('fw','1.0.0',b'firmware')
        self.assertEqual(simulate(artifact,b'firmware')['state'],'succeeded')
        self.assertEqual(simulate(artifact,b'badbytes')['state'],'failed')
    def test_each_failure_stage_remains_failed(self):
        artifact=describe('fw','1.0.0',b'x')
        for failure in ('transfer','verify','apply'):
            self.assertEqual(simulate(artifact,b'x',failure)['state'],'failed')
