from unittest.mock import patch

from edgeops.plugins import PluginHost
from tests.support import IsolatedCase, ROOT


class PluginFailureTests(IsolatedCase):
    def test_plugin_error_leaves_database_unchanged(self):
        host = PluginHost()
        host.load(ROOT / "plugins/import-jsonl")
        before = self.operations.database.path.read_bytes()
        with self.assertRaisesRegex(ValueError, "plugin failed"):
            host.invoke("import-jsonl", {"text": "{"})
        self.assertEqual(self.operations.database.path.read_bytes(), before)

    def test_workflow_plugin_error_has_failed_step_evidence(self):
        host = PluginHost()
        host.load(ROOT / "plugins/import-jsonl")
        self.workflows.plugins = host
        definition = self.workflow([{"id": "decode", "action": "plugin.invoke", "params": {"name": "import-jsonl", "request": {"text": "{"}}}])
        run_id = self.workflows.start(definition)
        result = self.workflows.resume(run_id)
        self.assertEqual(result["status"], "failed")
        self.assertIn("plugin failed", result["error"])
