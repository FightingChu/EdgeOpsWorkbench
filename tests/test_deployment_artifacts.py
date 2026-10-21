import unittest
from edgeops.domain.deployment.artifacts import Artifact,describe

class ArtifactTests(unittest.TestCase):
    def test_descriptor_matches_bytes(self):
        artifact=describe('sensor.bin','1.2.3',b'firmware')
        self.assertEqual(artifact.size,8); self.assertEqual(len(artifact.sha256),64)
    def test_traversal_and_empty_artifact_rejected(self):
        with self.assertRaises(ValueError): describe('../sensor','1.2.3',b'x')
        with self.assertRaises(ValueError): describe('sensor','1.2.3',b'')
