"""Read-only SQLite diagnostics that never initialize or migrate a target."""

from contextlib import contextmanager
from pathlib import Path
import sqlite3

from .migrations import SCHEMA_VERSION


@contextmanager
def readonly(path):
    resolved = Path(path).resolve()
    connection = sqlite3.connect(resolved.as_uri() + "?mode=ro", uri=True, timeout=5)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only=ON")
    try:
        yield connection
    finally:
        connection.close()


def inspect_database(path):
    with readonly(path) as connection:
        integrity = [row[0] for row in connection.execute("PRAGMA integrity_check")]
        foreign_keys = [list(row) for row in connection.execute("PRAGMA foreign_key_check")]
        row = connection.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()
        version = int(row[0]) if row else 0
        names = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        counts = {}
        for table in ("devices", "telemetry", "incidents", "events", "event_imports", "event_origins", "jobs", "job_runs", "schedules", "health_snapshots", "audit_entries", "workflow_runs", "workflow_steps", "firmware_artifacts", "deployments", "deployment_transitions"):
            if table in names:
                counts[table] = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        return {"ok": integrity == ["ok"] and not foreign_keys and 1 <= version <= SCHEMA_VERSION,
                "schema_version": version, "supported_version": SCHEMA_VERSION,
                "integrity": integrity, "foreign_key_violations": foreign_keys, "counts": counts,
                "page_count": connection.execute("PRAGMA page_count").fetchone()[0],
                "page_size": connection.execute("PRAGMA page_size").fetchone()[0]}
