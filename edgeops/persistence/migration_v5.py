"""Schema v5 adds durable firmware descriptors and compare-and-swap deployments."""
STATEMENTS=(
    '''CREATE TABLE firmware_artifacts(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,version TEXT NOT NULL,sha256 TEXT NOT NULL,size INTEGER NOT NULL,created_at TEXT NOT NULL,UNIQUE(name,version))''',
    '''CREATE TABLE deployments(id INTEGER PRIMARY KEY AUTOINCREMENT,device_id TEXT NOT NULL REFERENCES devices(id),artifact_id INTEGER NOT NULL REFERENCES firmware_artifacts(id),state TEXT NOT NULL,revision INTEGER NOT NULL,received_bytes INTEGER NOT NULL DEFAULT 0,error TEXT,created_at TEXT NOT NULL,updated_at TEXT NOT NULL)''',
    '''CREATE TABLE deployment_transitions(id INTEGER PRIMARY KEY AUTOINCREMENT,deployment_id INTEGER NOT NULL REFERENCES deployments(id),revision INTEGER NOT NULL,action TEXT NOT NULL,from_state TEXT NOT NULL,to_state TEXT NOT NULL,created_at TEXT NOT NULL,UNIQUE(deployment_id,revision))''',
    'CREATE INDEX deployments_device ON deployments(device_id,id DESC)',
)

def migrate_v5(connection):
    for statement in STATEMENTS: connection.execute(statement)
