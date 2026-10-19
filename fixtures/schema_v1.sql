-- Released v1 database with device, reading, and aggregated incident history.
CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
INSERT INTO meta VALUES('schema_version','1');
CREATE TABLE devices(id TEXT PRIMARY KEY,name TEXT NOT NULL,kind TEXT NOT NULL,status TEXT NOT NULL,last_seen TEXT,created_at TEXT NOT NULL);
CREATE TABLE telemetry(id INTEGER PRIMARY KEY AUTOINCREMENT,device_id TEXT NOT NULL REFERENCES devices(id),metric TEXT NOT NULL,value REAL NOT NULL,unit TEXT NOT NULL,recorded_at TEXT NOT NULL);
CREATE INDEX telemetry_device_time ON telemetry(device_id,recorded_at DESC);
CREATE TABLE incidents(id INTEGER PRIMARY KEY AUTOINCREMENT,device_id TEXT NOT NULL REFERENCES devices(id),fingerprint TEXT NOT NULL,title TEXT NOT NULL,severity TEXT NOT NULL,status TEXT NOT NULL,occurrences INTEGER NOT NULL,first_seen TEXT NOT NULL,last_seen TEXT NOT NULL,UNIQUE(device_id,fingerprint,status));
CREATE INDEX incidents_status_time ON incidents(status,last_seen DESC);
INSERT INTO devices VALUES('legacy-01','Legacy sensor','sensor','online','2026-10-19T09:00:00+00:00','2026-10-18T09:00:00+00:00');
INSERT INTO telemetry VALUES(7,'legacy-01','temperature',89.0,'C','2026-10-19T09:00:00+00:00');
INSERT INTO incidents VALUES(2,'legacy-01','threshold:temperature:critical','temperature threshold exceeded','critical','open',3,'2026-10-18T09:00:00+00:00','2026-10-19T09:00:00+00:00');
