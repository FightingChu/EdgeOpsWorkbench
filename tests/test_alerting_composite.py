import unittest
from edgeops.domain.alerting.composite import evaluate_tree

class CompositeTests(unittest.TestCase):
    def test_nested_boolean_rule(self):
        atom={'field':'s','op':'eq','value':'ok'}
        self.assertTrue(evaluate_tree({'s':'ok'},{'all':[atom,{'not':{'field':'s','op':'eq','value':'bad'}}]}))
    def test_deep_tree_rejected(self):
        tree={'field':'x','op':'eq','value':1}
        for _ in range(10): tree={'not':tree}
        with self.assertRaises(ValueError): evaluate_tree({'x':1},tree)
