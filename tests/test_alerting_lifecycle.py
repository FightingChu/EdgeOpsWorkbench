import unittest
from edgeops.domain.alerting.lifecycle import transition

class LifecycleTests(unittest.TestCase):
    def test_acknowledge_resolve_and_reopen(self):
        state=transition('open','ack')
        self.assertEqual(transition(state,'resolve'),'resolved')
        self.assertEqual(transition('resolved','reopen'),'open')
    def test_illegal_transition_rejected(self):
        with self.assertRaises(ValueError): transition('resolved','ack')
