import unittest
from dataclasses import asdict
from edgeops.domain.deployment.artifacts import describe
from edgeops.domain.deployment.manifests import validate_manifest

class FirmwareManifestTests(unittest.TestCase):
    def manifest(self): return {'version':1,'artifact':asdict(describe('fw.bin','2.0.0',b'x')),'device_kind':'sensor','minimum_version':'1.0.0'}
    def test_canonical_manifest(self):
        self.assertEqual(validate_manifest(self.manifest())['artifact']['size'],1)
    def test_future_manifest_rejected(self):
        with self.assertRaises(ValueError): validate_manifest({**self.manifest(),'version':2})
