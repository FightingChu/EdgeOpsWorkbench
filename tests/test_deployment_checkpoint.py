import unittest
from edgeops.domain.deployment.checkpoint import create,validate

class TransferCheckpointTests(unittest.TestCase):
    def test_resume_uses_verified_prefix(self):
        self.assertEqual(validate(b'abcd',create(b'abcd',2)),2)
    def test_changed_artifact_or_prefix_rejected(self):
        checkpoint=create(b'abcd',2)
        with self.assertRaises(ValueError): validate(b'abce',checkpoint)
        checkpoint['prefix_sha256']='0'*64
        with self.assertRaises(ValueError): validate(b'abcd',checkpoint)
