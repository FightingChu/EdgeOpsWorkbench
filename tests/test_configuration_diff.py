import unittest
from edgeops.configuration.diff import changes

class ConfigDiffTests(unittest.TestCase):
    def test_added_removed_and_nested_values(self):
        result=changes({'api':{'port':1},'old':True},{'api':{'port':2},'new':3})
        self.assertEqual([x['op'] for x in result],['replace','add','remove'])
        self.assertEqual(result[0]['path'],'api.port')
    def test_type_change_is_visible(self):
        self.assertEqual(changes({'x':True},{'x':1})[0]['op'],'replace')
