import unittest
from edgeops.domain.alerting.escalation import severity_for

class EscalationTests(unittest.TestCase):
    def test_escalates_without_lowering_base(self):
        self.assertEqual(severity_for('warning',5,[(3,'error'),(10,'critical')]),'error')
        self.assertEqual(severity_for('critical',1,[(1,'info')]),'critical')
    def test_unknown_severity_rejected(self):
        with self.assertRaises(ValueError): severity_for('warning',1,[(1,'fatal')])
