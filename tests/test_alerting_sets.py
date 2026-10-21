import unittest
from edgeops.domain.alerting.sets import member

class MembershipTests(unittest.TestCase):
    def test_type_aware_membership_and_negation(self):
        self.assertFalse(member(True,[1]))
        self.assertTrue(member('east',['east','west']))
        self.assertTrue(member('north',['east'],True))
    def test_unbounded_set_rejected(self):
        with self.assertRaises(ValueError): member('a',['a']*101)
