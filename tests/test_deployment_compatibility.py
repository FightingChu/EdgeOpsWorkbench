import unittest
from edgeops.domain.deployment.compatibility import check,version_tuple

class FirmwareCompatibilityTests(unittest.TestCase):
    def test_numeric_version_and_downgrade(self):
        self.assertGreater(version_tuple('1.10.0'),version_tuple('1.2.0'))
        device={'kind':'sensor','version':'2.0.0','online':True}
        manifest={'device_kind':'sensor','minimum_version':'1.0.0','artifact':{'version':'1.0.0'}}
        self.assertFalse(check(device,manifest)['compatible']); self.assertTrue(check(device,manifest,True)['compatible'])
    def test_version_injection_rejected(self):
        with self.assertRaises(ValueError): version_tuple('1.0.0;run')
