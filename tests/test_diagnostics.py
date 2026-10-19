from edgeops.persistence.diagnostics import inspect_database
from tests.support import IsolatedCase


class DiagnosticTests(IsolatedCase):
    def test_report_is_readonly_and_redacted(self):
        before = self.operations.database.path.read_bytes()
        report = inspect_database(self.operations.database.path)
        self.assertTrue(report["ok"])
        self.assertEqual(report["counts"]["events"], 0)
        self.assertNotIn(str(self.root), str(report))
        self.assertEqual(before, self.operations.database.path.read_bytes())

    def test_missing_target_does_not_create_file(self):
        import sqlite3
        missing = self.root / "missing.sqlite3"
        with self.assertRaises(sqlite3.OperationalError):
            inspect_database(missing)
        self.assertFalse(missing.exists())
