"""Bounded database operations for devices, telemetry, and incidents."""

from datetime import datetime, timezone


def utc_now():
    return datetime.now(timezone.utc).isoformat()


class OperationsRepository:
    @staticmethod
    def register_device(connection, device):
        connection.execute(
            """INSERT INTO devices(id,name,kind,status,created_at)
               VALUES(?,?,?,'online',?)
               ON CONFLICT(id) DO UPDATE SET name=excluded.name,kind=excluded.kind,status='online'""",
            (device.id, device.name, device.kind, utc_now()),
        )

    @staticmethod
    def ingest(connection, reading, decision):
        exists = connection.execute("SELECT 1 FROM devices WHERE id=?", (reading.device_id,)).fetchone()
        if exists is None:
            raise ValueError("device is not registered")
        cursor = connection.execute(
            "INSERT INTO telemetry(device_id,metric,value,unit,recorded_at) VALUES(?,?,?,?,?)",
            (reading.device_id, reading.metric, reading.value, reading.unit, reading.recorded_at),
        )
        connection.execute(
            "UPDATE devices SET status='online',last_seen=? WHERE id=?",
            (reading.recorded_at, reading.device_id),
        )
        if decision:
            connection.execute(
                """INSERT INTO incidents(device_id,fingerprint,title,severity,status,occurrences,first_seen,last_seen)
                   VALUES(?,?,?,?, 'open',1,?,?)
                   ON CONFLICT(device_id,fingerprint,status) DO UPDATE SET
                     occurrences=incidents.occurrences+1,
                     severity=excluded.severity,
                     last_seen=excluded.last_seen""",
                (reading.device_id, decision.fingerprint, decision.title, decision.severity,
                 reading.recorded_at, reading.recorded_at),
            )
        return cursor.lastrowid

    @staticmethod
    def summary(connection):
        counts = {}
        for key, query in {
            "devices": "SELECT COUNT(*) FROM devices",
            "telemetry": "SELECT COUNT(*) FROM telemetry",
            "open_incidents": "SELECT COUNT(*) FROM incidents WHERE status='open'",
            "critical_incidents": "SELECT COUNT(*) FROM incidents WHERE status='open' AND severity='critical'",
        }.items():
            counts[key] = connection.execute(query).fetchone()[0]
        return counts

    @staticmethod
    def devices(connection):
        return [dict(row) for row in connection.execute(
            "SELECT id,name,kind,status,last_seen,created_at FROM devices ORDER BY name,id"
        )]

    @staticmethod
    def incidents(connection):
        return [dict(row) for row in connection.execute(
            """SELECT id,device_id,title,severity,status,occurrences,first_seen,last_seen
               FROM incidents ORDER BY CASE severity WHEN 'critical' THEN 0 ELSE 1 END,last_seen DESC,id"""
        )]

    @staticmethod
    def telemetry(connection, limit=50):
        if type(limit) is not int or not 1 <= limit <= 200:
            raise ValueError("limit must be an integer between 1 and 200")
        return [dict(row) for row in connection.execute(
            """SELECT id,device_id,metric,value,unit,recorded_at
               FROM telemetry ORDER BY recorded_at DESC,id DESC LIMIT ?""",
            (limit,),
        )]

    @staticmethod
    def incident(connection, incident_id):
        row = connection.execute("SELECT * FROM incidents WHERE id=?", (incident_id,)).fetchone()
        return dict(row) if row else None

    @staticmethod
    def incident_telemetry(connection, incident, limit):
        metric = incident["fingerprint"].split(":")[1]
        return [dict(row) for row in connection.execute(
            """SELECT id,device_id,metric,value,unit,recorded_at FROM telemetry
               WHERE device_id=? AND metric=? ORDER BY recorded_at DESC,id DESC LIMIT ?""",
            (incident["device_id"], metric, limit),
        )]
