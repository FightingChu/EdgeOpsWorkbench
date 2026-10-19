"""Operator-facing redacted diagnostics and bounded history queries."""

import json

from ..domain.validation import integer
from ..persistence.audit import recent
from ..persistence.diagnostics import inspect_database


class DiagnosticsService:
    def __init__(self, operations):
        self.database = operations.database

    def report(self):
        return inspect_database(self.database.path)

    def audit(self, limit=100):
        with self.database.connect() as connection:
            return recent(connection, limit)

    def health_history(self, limit=50):
        integer(limit, "limit", 1, 200)
        with self.database.connect() as connection:
            return [{"job_id": row["job_id"], "recorded_at": row["recorded_at"],
                     "snapshot": json.loads(row["snapshot_json"])} for row in connection.execute(
                "SELECT * FROM health_snapshots ORDER BY id DESC LIMIT ?", (limit,))]
