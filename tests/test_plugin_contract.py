import json

from edgeops.domain.plugins import PluginManifest
from edgeops.plugins import PluginHost
from tests.support import IsolatedCase, ROOT


class PluginContractTests(IsolatedCase):
    def test_capabilities_and_entrypoint_are_validated(self):
        manifest = json.loads((ROOT / "plugins/import-jsonl/plugin.json").read_text())
        for key, value in (("version", 2), ("entrypoint", "../evil.py:invoke"), ("capabilities", ["filesystem.write"])):
            with self.subTest(key=key), self.assertRaises(ValueError):
                PluginManifest.parse({**manifest, key: value})

    def test_duplicate_names_are_rejected(self):
        host = PluginHost()
        host.load(ROOT / "plugins/import-jsonl")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            host.load(ROOT / "plugins/import-jsonl")
