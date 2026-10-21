import unittest
from edgeops.configuration.reload import ConfigRevision

class ConfigReloadTests(unittest.TestCase):
    def test_generation_only_changes_for_valid_new_values(self):
        state=ConfigRevision({'port':8877}); old=state.fingerprint
        self.assertFalse(state.update({'port':8877}))
        self.assertTrue(state.update({'port':9000}))
        self.assertEqual(state.generation,2); self.assertNotEqual(state.fingerprint,old)
    def test_invalid_update_keeps_previous_configuration(self):
        state=ConfigRevision({})
        with self.assertRaises(ValueError): state.update({'port':0})
        self.assertEqual(state.values['port'],8877)
