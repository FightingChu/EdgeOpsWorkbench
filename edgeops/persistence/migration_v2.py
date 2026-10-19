"""Schema v2: immutable events, successful import audit, and record provenance."""

STATEMENTS = (
    """CREATE TABLE event_imports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL, format TEXT NOT NULL, encoding TEXT NOT NULL,
        ingest_version INTEGER NOT NULL, sha256 TEXT NOT NULL,
        byte_count INTEGER NOT NULL, physical_lines INTEGER NOT NULL,
        record_count INTEGER NOT NULL, inserted_count INTEGER NOT NULL,
        duplicate_count INTEGER NOT NULL, imported_at TEXT NOT NULL,
        CHECK(record_count = inserted_count + duplicate_count)
    )""",
    """CREATE TABLE events(
        id INTEGER PRIMARY KEY AUTOINCREMENT, fingerprint TEXT NOT NULL UNIQUE,
        message TEXT NOT NULL, severity TEXT NOT NULL, service TEXT NOT NULL,
        device_id TEXT, recorded_at TEXT, kind TEXT NOT NULL, metadata_json TEXT NOT NULL
    )""",
    """CREATE TABLE event_origins(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER NOT NULL REFERENCES events(id),
        import_id INTEGER NOT NULL REFERENCES event_imports(id),
        physical_line INTEGER NOT NULL, byte_offset INTEGER NOT NULL,
        byte_length INTEGER NOT NULL, raw_record TEXT NOT NULL,
        UNIQUE(import_id, physical_line)
    )""",
    "CREATE INDEX event_origins_event ON event_origins(event_id,id)",
    "CREATE INDEX events_severity ON events(severity,id DESC)",
    "CREATE INDEX events_service ON events(service,id DESC)",
    "CREATE INDEX events_device ON events(device_id,id DESC)",
    "CREATE INDEX events_time ON events(recorded_at,id DESC)",
)


def migrate_v2(connection):
    for statement in STATEMENTS:
        connection.execute(statement)
