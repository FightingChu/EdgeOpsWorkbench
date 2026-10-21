import unittest
from edgeops.domain.deployment.policy import RolloutPolicy,may_continue

class RolloutPolicyTests(unittest.TestCase):
    def test_failure_budget_boundary(self):
        policy=RolloutPolicy(max_failures=1)
        self.assertTrue(may_continue(5,1,policy)); self.assertFalse(may_continue(5,2,policy))
    def test_zero_batch_rejected(self):
        with self.assertRaises(ValueError): RolloutPolicy(batch_size=0)
