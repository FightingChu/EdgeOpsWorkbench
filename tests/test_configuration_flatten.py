import unittest
from edgeops.configuration.flatten import flatten,expand

class ConfigFlattenTests(unittest.TestCase):
    def test_round_trip_empty_objects_and_arrays(self):
        value={'a':{'b':[1,2],'c':{}}}
        self.assertEqual(expand(flatten(value)),value)
    def test_ambiguous_and_conflicting_paths(self):
        with self.assertRaises(ValueError): flatten({'a.b':1})
        with self.assertRaises(ValueError): expand({'a':1,'a.b':2})
