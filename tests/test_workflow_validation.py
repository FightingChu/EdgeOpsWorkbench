import copy

from tests.support import IsolatedCase


class WorkflowGrammarTests(IsolatedCase):
    def test_dry_run_creates_no_persistent_runs(self):
        self.assertTrue(self.workflows.dry_run(self.workflow())["valid"])
        with self.operations.database.connect() as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM workflow_runs").fetchone()[0], 0)

    def test_forward_refs_duplicate_ids_and_future_versions_fail(self):
        definitions = []
        for change in ("forward", "duplicate", "version", "unknown"):
            value = copy.deepcopy(self.workflow())
            if change == "forward":
                value["steps"][0]["params"] = {"value": {"$ref": "steps.check.matched"}}
            elif change == "duplicate":
                value["steps"][1]["id"] = "first"
            elif change == "version":
                value["version"] = 2
            else:
                value["steps"][0]["action"] = "shell.execute"
            definitions.append(value)
        for definition in definitions:
            with self.subTest(definition=definition), self.assertRaises(ValueError):
                self.workflows.start(definition)
