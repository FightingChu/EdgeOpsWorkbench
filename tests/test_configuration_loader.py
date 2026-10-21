import unittest
import json,tempfile
from pathlib import Path
from edgeops.configuration.loader import load

class ConfigLoaderTests(unittest.TestCase):
    def test_file_environment_and_override_precedence(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/'config.json'; path.write_text(json.dumps({'port':8000}))
            self.assertEqual(load([path],{'EDGEOPS_PORT':'9000'},{'port':9100})['port'],9100)
    def test_invalid_json_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            path=Path(root)/'config.json'; path.write_text('[')
            with self.assertRaises(ValueError): load([path])
