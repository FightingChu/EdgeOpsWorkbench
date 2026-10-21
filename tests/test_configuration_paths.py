import unittest
from pathlib import Path
import tempfile
from edgeops.configuration.paths import resolve_within

class ConfigPathTests(unittest.TestCase):
    def test_relative_path_is_resolved(self):
        with tempfile.TemporaryDirectory() as root:
            self.assertEqual(resolve_within(root,'data/logs').parent,Path(root).resolve()/'data')
    def test_parent_escape_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError): resolve_within(root,'../secret')
