"""Atomic event imports and keyset queries with a fixed insertion snapshot."""

import json

from ..domain.events import INGEST_VERSION, SEVERITIES
from .repositories import utc_now


class EventRepository:
    @staticmethod
    def import_file(connection, parsed):
        cursor = connection.execute(
            """INSERT INTO event_imports(source,format,encoding,ingest_version,sha256,
               byte_count,physical_lines,record_count,inserted_count,duplicate_count,imported_at)
               VALUES(?,?,?,?,?,?,?,0,0,0,?)""",
            (parsed.source, parsed.format, parsed.encoding, INGEST_VERSION, parsed.sha256,
             parsed.byte_count, parsed.physical_lines, utc_now()),
        )
        import_id = cursor.lastrowid
        inserted = 0
        for record in parsed.records:
            event = record.event
            fingerprint = event.fingerprint
            cursor = connection.execute(
                """INSERT INTO events(fingerprint,message,severity,service,device_id,
                   recorded_at,kind,metadata_json) VALUES(?,?,?,?,?,?,?,?)
                   ON CONFLICT(fingerprint) DO NOTHING""",
                (fingerprint, event.message, event.severity, event.service, event.device_id,
                 event.recorded_at, event.kind, event.metadata_json),
            )
            if cursor.rowcount:
                event_id = cursor.lastrowid
                inserted += 1
            else:
                event_id = connection.execute(
                    "SELECT id FROM events WHERE fingerprint=?", (fingerprint,)
                ).fetchone()[0]
            connection.execute(
                """INSERT INTO event_origins(event_id,import_id,physical_line,byte_offset,
                   byte_length,raw_record) VALUES(?,?,?,?,?,?)""",
                (event_id, import_id, record.physical_line, record.byte_offset,
                 record.byte_length, record.raw_record),
            )
        count = len(parsed.records)
        connection.execute(
            "UPDATE event_imports SET record_count=?,inserted_count=?,duplicate_count=? WHERE id=?",
            (count, inserted, count - inserted, import_id),
        )
        return dict(connection.execute("SELECT * FROM event_imports WHERE id=?", (import_id,)).fetchone())

    @staticmethod
    def page(connection, query):
        position = query.position()
        snapshot, before = position if position else (
            connection.execute("SELECT COALESCE(MAX(id),0) FROM events").fetchone()[0], None
        )
        clauses = ["e.id <= ?"]
        values = [snapshot]
        if before is not None:
            clauses.append("e.id < ?")
            values.append(before)
        for name in ("severity", "service", "device_id"):
            if getattr(query, name) is not None:
                clauses.append(f"e.{name} = ?")
                values.append(getattr(query, name))
        for name, operator in (("since", ">="), ("until", "<=")):
            if getattr(query, name) is not None:
                clauses.append(f"e.recorded_at {operator} ?")
                values.append(getattr(query, name))
        if query.q is not None:
            clauses.append("e.message LIKE ? ESCAPE '\\'")
            literal = query.q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            values.append("%" + literal + "%")
        values.append(query.limit + 1)
        rows = connection.execute(
            """SELECT e.*,o.import_id,o.physical_line,o.byte_offset,o.byte_length,
                      i.source,i.encoding,i.ingest_version
               FROM events e
               JOIN event_origins o ON o.id=(SELECT MIN(id) FROM event_origins WHERE event_id=e.id)
               JOIN event_imports i ON i.id=o.import_id WHERE """ + " AND ".join(clauses) +
            " ORDER BY e.id DESC LIMIT ?", values,
        ).fetchall()
        has_more = len(rows) > query.limit
        events = []
        for row in rows[:query.limit]:
            event = dict(row)
            event["metadata"] = json.loads(event.pop("metadata_json"))
            events.append(event)
        return {"events": events, "snapshot_id": snapshot, "next_cursor":
                query.next_cursor(snapshot, events[-1]["id"]) if has_more else None}

    @staticmethod
    def filters(connection):
        result = {"severities": list(SEVERITIES), "truncated": {}}
        for name, column in (("services", "service"), ("devices", "device_id")):
            rows = connection.execute(
                f"SELECT DISTINCT {column} FROM events WHERE {column} IS NOT NULL ORDER BY {column} LIMIT 201"
            ).fetchall()
            result[name] = [row[0] for row in rows[:200]]
            result["truncated"][name] = len(rows) > 200
        return result
