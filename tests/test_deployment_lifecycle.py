import unittest
from edgeops.domain.deployment.lifecycle import transition,terminal

class DeploymentLifecycleTests(unittest.TestCase):
    def test_transfer_verify_apply_chain(self):
        state='queued'
        for action in ('start','transferred','verified','applied'): state=transition(state,action)
        self.assertEqual(state,'succeeded'); self.assertTrue(terminal(state))
    def test_cannot_skip_verification(self):
        with self.assertRaises(ValueError): transition('transferring','applied')
