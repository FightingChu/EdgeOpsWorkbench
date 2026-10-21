"""Artifact descriptors are verified against the exact supplied file bytes."""
from edgeops.application.artifacts import ArtifactService
from tests.support import IsolatedCase

class ArtifactServiceTests(IsolatedCase):
    def test_verified_payload_and_corruption(self):
        path=self.root/'firmware.bin';path.write_bytes(b'firmware');service=ArtifactService()
        artifact=service.inspect(path,'1.0.0')
        self.assertEqual(service.verified_bytes(path,artifact),b'firmware')
        path.write_bytes(b'corrupted')
        with self.assertRaises(ValueError): service.verified_bytes(path,artifact)
    def test_empty_file_rejected(self):
        path=self.root/'firmware.bin';path.write_bytes(b'')
        with self.assertRaises(ValueError): ArtifactService().inspect(path,'1.0.0')
