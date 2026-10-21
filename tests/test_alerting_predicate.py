import unittest
from edgeops.domain.alerting.predicate import evaluate

class PredicateTests(unittest.TestCase):
    def test_dispatches_numeric_and_severity(self):
        self.assertTrue(evaluate({'value':90},{'field':'value','op':'gt','value':85}))
        self.assertTrue(evaluate({'severity':'critical'},{'field':'severity','op':'severity','value':'error'}))
    def test_unknown_operator_rejected(self):
        with self.assertRaises(ValueError): evaluate({'x':1},{'field':'x','op':'execute','value':1})
