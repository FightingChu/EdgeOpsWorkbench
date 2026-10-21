import unittest
from edgeops.configuration.merging import merge_layers

class ConfigMergeTests(unittest.TestCase):
    def test_deep_override_does_not_mutate_source(self):
        base={'api':{'port':8877,'tags':['a']}}
        result=merge_layers(base,{'api':{'port':9000}})
        result['api']['tags'].append('b')
        self.assertEqual(base['api']['tags'],['a'])
        self.assertEqual(result['api']['port'],9000)
    def test_object_scalar_conflict(self):
        with self.assertRaises(ValueError): merge_layers({'a':1},{'a':{'b':2}})
