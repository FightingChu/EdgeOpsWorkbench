import unittest
from edgeops.domain.deployment.progress import transfer,fleet

class DeploymentProgressTests(unittest.TestCase):
    def test_progress_and_failure_are_distinct(self):
        self.assertEqual(transfer(100,25)['percent'],25)
        self.assertEqual(fleet(['succeeded','failed'])['succeeded'],1)
    def test_overreported_bytes_rejected(self):
        with self.assertRaises(ValueError): transfer(10,11)
