"""Versioned SQLite schema migrations."""

from .migration_v2 import migrate_v2
from .migration_v3 import migrate_v3
from .migration_v4 import migrate_v4

SCHEMA_VERSION = 4


def _execute_schema(connection, script):
    # executescript commits an active transaction. Execute the unchanged v1 DDL
    # individually so both initial creation and later migrations roll back together.
    for statement in script.split(";"):
        if statement.strip():
            connection.execute(statement)


def migrate(connection):
    connection.execute("CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL)")
    row = connection.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()
    version = int(row[0]) if row else 0
    if version > SCHEMA_VERSION:
        raise RuntimeError(f"database schema {version} is newer than supported version {SCHEMA_VERSION}")
    if version < 1:
        _execute_schema(connection,
            """
            CREATE TABLE devices(
              id TEXT PRIMARY KEY,
              name TEXT NOT NULL,
              kind TEXT NOT NULL,
              status TEXT NOT NULL,
              last_seen TEXT,
              created_at TEXT NOT NULL
            );
            CREATE TABLE telemetry(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              device_id TEXT NOT NULL REFERENCES devices(id),
              metric TEXT NOT NULL,
              value REAL NOT NULL,
              unit TEXT NOT NULL,
              recorded_at TEXT NOT NULL
            );
            CREATE INDEX telemetry_device_time ON telemetry(device_id,recorded_at DESC);
            CREATE TABLE incidents(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              device_id TEXT NOT NULL REFERENCES devices(id),
              fingerprint TEXT NOT NULL,
              title TEXT NOT NULL,
              severity TEXT NOT NULL,
              status TEXT NOT NULL,
              occurrences INTEGER NOT NULL,
              first_seen TEXT NOT NULL,
              last_seen TEXT NOT NULL,
              UNIQUE(device_id,fingerprint,status)
            );
            CREATE INDEX incidents_status_time ON incidents(status,last_seen DESC);
            """
        )
    if version < 2:
        migrate_v2(connection)
    if version < 3:
        migrate_v3(connection)
    if version < 4:
        migrate_v4(connection)
    connection.execute(
        "INSERT INTO meta(key,value) VALUES('schema_version',?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (str(SCHEMA_VERSION),),
    )
