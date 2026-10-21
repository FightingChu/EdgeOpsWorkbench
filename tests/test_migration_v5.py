"""Migration v5 preserves v4 rows and rolls back failed extension DDL."""
import sqlite3
from unittest.mock import patch
from edgeops.persistence import migrations
from edgeops.persistence.migration_v4 import migrate_v4
from edgeops.persistence.database import Database
from tests.support import IsolatedCase

class MigrationV5Tests(IsolatedCase):
    def test_v4_upgrade_preserves_workflow_rows(self):
        path=self.root/'v4.sqlite3'
        with sqlite3.connect(path) as connection:
            connection.execute('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT NOT NULL)')
            connection.execute("INSERT INTO meta VALUES('schema_version','4')")
            connection.execute('CREATE TABLE devices(id TEXT PRIMARY KEY)')
            migrate_v4(connection)
            connection.execute("INSERT INTO workflow_runs(definition_json,input_json,status,created_at,updated_at) VALUES('{}','{}','pending','a','a')")
        Database(path).initialize()
        with Database(path).connect() as connection:
            self.assertEqual(connection.execute('SELECT COUNT(*) FROM workflow_runs').fetchone()[0],1)
            self.assertEqual(connection.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()[0],'5')
            self.assertEqual(connection.execute('PRAGMA foreign_key_check').fetchall(),[])
    def test_extension_failure_rolls_back_tables_and_version(self):
        path=self.root/'failed.sqlite3'
        def failure(connection):
            connection.execute('CREATE TABLE transient_marker(id INTEGER)')
            raise RuntimeError('injected')
        with patch.object(migrations,'migrate_v5',failure),self.assertRaises(RuntimeError): Database(path).initialize()
        with Database(path).connect() as connection:
            self.assertEqual(connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall(),[])
