from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from edgeops.persistence.database import Database
from edgeops.persistence import migrations


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "db.sqlite3"

    def tearDown(self):
        self.tmp.cleanup()

    def test_upgrade_preserves_released_v1_rows(self):
        fixture = Path(__file__).resolve().parents[1] / "fixtures" / "schema_v1.sql"
        with sqlite3.connect(self.path) as connection:
            connection.executescript(fixture.read_text(encoding="utf-8"))
        Database(self.path).initialize()
        with sqlite3.connect(self.path) as connection:
            self.assertEqual(connection.execute("SELECT value FROM meta").fetchone()[0], str(migrations.SCHEMA_VERSION))
            self.assertEqual(connection.execute("SELECT value FROM telemetry").fetchone()[0], 89.0)
            self.assertEqual(connection.execute("SELECT occurrences FROM incidents").fetchone()[0], 3)
            self.assertEqual(connection.execute("PRAGMA foreign_key_check").fetchall(), [])

    def test_newer_schema_rejected_without_mutation(self):
        with sqlite3.connect(self.path) as connection:
            connection.execute("CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT NOT NULL)")
            connection.execute("INSERT INTO meta VALUES('schema_version','999')")
        before = self.path.read_bytes()
        with self.assertRaisesRegex(RuntimeError, "newer"):
            Database(self.path).initialize()
        self.assertEqual(before, self.path.read_bytes())

    def test_failed_migration_rolls_back_all_ddl_and_version(self):
        def fail(connection):
            connection.execute("CREATE TABLE should_rollback(id INTEGER)")
            raise RuntimeError("injected failure")
        with patch.object(migrations, "migrate_v2", fail):
            with self.assertRaises(RuntimeError):
                Database(self.path).initialize()
        with sqlite3.connect(self.path) as connection:
            self.assertEqual(connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall(), [])
