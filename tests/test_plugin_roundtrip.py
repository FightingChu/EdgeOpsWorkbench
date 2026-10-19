from edgeops.plugins import PluginHost
from tests.support import IsolatedCase, ROOT


class PluginRoundtripTests(IsolatedCase):
    def test_import_export_import_is_symmetric(self):
        host = PluginHost()
        host.load(ROOT / "plugins/import-jsonl")
        host.load(ROOT / "plugins/export-jsonl")
        text = '{"message":"海鸥","severity":"warning","recorded_at":"2026-10-19T17:00:00+08:00","extra":{"b":2,"a":1}}\n'
        first = host.invoke("import-jsonl", {"text": text})
        exported = host.invoke("export-jsonl", first)
        second = host.invoke("import-jsonl", exported)
        self.assertEqual(second, first)
        self.assertEqual(first["events"][0]["message"], "海鸥")
