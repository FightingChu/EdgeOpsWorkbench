import unittest
from edgeops.domain.deployment.artifacts import describe
from edgeops.domain.deployment.rollback import rollback_plan

class FirmwareRollbackTests(unittest.TestCase):
    def test_verified_previous_version(self):
        artifact=describe('fw','1.0.0',b'old')
        self.assertEqual(rollback_plan('a',artifact,b'old','2.0.0')['to_version'],'1.0.0')
    def test_corrupted_previous_image_rejected(self):
        with self.assertRaises(ValueError): rollback_plan('a',describe('fw','1.0.0',b'old'),b'bad','2.0.0')
