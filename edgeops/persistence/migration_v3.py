"""Schema v3: leased jobs, periodic checks, health history, and mutation audit."""

STATEMENTS = (
    """CREATE TABLE audit_entries(id INTEGER PRIMARY KEY AUTOINCREMENT,
       action TEXT NOT NULL,target TEXT NOT NULL,details_json TEXT NOT NULL,created_at TEXT NOT NULL)""",
    """CREATE TABLE jobs(id INTEGER PRIMARY KEY AUTOINCREMENT,action TEXT NOT NULL,
       payload_json TEXT NOT NULL,due_at REAL NOT NULL,max_attempts INTEGER NOT NULL,
       retry_delay INTEGER NOT NULL,dedup_key TEXT UNIQUE,status TEXT NOT NULL,
       attempts INTEGER NOT NULL DEFAULT 0,lease_token TEXT,lease_until REAL,
       result_json TEXT,error TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL)""",
    "CREATE INDEX jobs_due ON jobs(status,due_at,id)",
    """CREATE TABLE job_runs(id INTEGER PRIMARY KEY AUTOINCREMENT,
       job_id INTEGER NOT NULL REFERENCES jobs(id),attempt INTEGER NOT NULL,
       lease_token TEXT NOT NULL UNIQUE,started_at REAL NOT NULL,finished_at REAL,
       status TEXT NOT NULL,error TEXT,UNIQUE(job_id,attempt))""",
    """CREATE TABLE schedules(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL UNIQUE,
       action TEXT NOT NULL,payload_json TEXT NOT NULL,interval INTEGER NOT NULL,
       next_run REAL NOT NULL,enabled INTEGER NOT NULL DEFAULT 1)""",
    """CREATE TABLE health_snapshots(id INTEGER PRIMARY KEY AUTOINCREMENT,
       job_id INTEGER NOT NULL UNIQUE REFERENCES jobs(id),recorded_at REAL NOT NULL,
       snapshot_json TEXT NOT NULL)""",
)


def migrate_v3(connection):
    for statement in STATEMENTS:
        connection.execute(statement)
