"""Schema v4: resumable workflow runs and durable individual step results."""

STATEMENTS = (
    """CREATE TABLE workflow_runs(id INTEGER PRIMARY KEY AUTOINCREMENT,
       definition_json TEXT NOT NULL,input_json TEXT NOT NULL,status TEXT NOT NULL,
       current_step INTEGER NOT NULL DEFAULT 0,lease_token TEXT,lease_until REAL,
       error TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL)""",
    """CREATE TABLE workflow_steps(id INTEGER PRIMARY KEY AUTOINCREMENT,
       run_id INTEGER NOT NULL REFERENCES workflow_runs(id),step_id TEXT NOT NULL,
       position INTEGER NOT NULL,status TEXT NOT NULL,attempts INTEGER NOT NULL,
       result_json TEXT,error TEXT,UNIQUE(run_id,position))""",
    "CREATE INDEX workflow_status ON workflow_runs(status,id)",
)


def migrate_v4(connection):
    for statement in STATEMENTS:
        connection.execute(statement)
