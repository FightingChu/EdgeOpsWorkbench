"""Periodic dispatch creates one idempotent job per scheduled instant."""

from ..domain.jobs import JobRequest
from ..domain.validation import integer
from . import jobs
from .audit import record


def create(connection, schedule):
    cursor = connection.execute(
        "INSERT INTO schedules(name,action,payload_json,interval,next_run) VALUES(?,?,?,?,?)",
        (schedule.name, schedule.action, schedule.payload_json, schedule.interval, schedule.next_run),
    )
    record(connection, "schedule.create", cursor.lastrowid, {"name": schedule.name})
    return cursor.lastrowid


def dispatch(connection, now, limit=100):
    integer(limit, "limit", 1, 200)
    result = []
    for _ in range(limit):
        schedule = connection.execute("SELECT * FROM schedules WHERE enabled=1 AND next_run<=? ORDER BY next_run,id LIMIT 1", (now,)).fetchone()
        if schedule is None:
            break
        request = JobRequest(schedule["action"], schedule["payload_json"], schedule["next_run"],
                             dedup_key=f"schedule:{schedule['id']}:{schedule['next_run']:.6f}")
        result.append(jobs.enqueue(connection, request))
        connection.execute("UPDATE schedules SET next_run=next_run+interval WHERE id=?", (schedule["id"],))
        record(connection, "schedule.dispatch", schedule["id"], {"job_id": result[-1], "due_at": schedule["next_run"]})
    return result


def set_enabled(connection, schedule_id, enabled):
    if type(enabled) is not bool:
        raise ValueError("enabled must be a boolean")
    cursor = connection.execute("UPDATE schedules SET enabled=? WHERE id=?", (int(enabled), schedule_id))
    if not cursor.rowcount:
        raise ValueError("schedule not found")
    record(connection, "schedule.enable", schedule_id, {"enabled": enabled})


def list_schedules(connection):
    return [dict(row) for row in connection.execute("SELECT * FROM schedules ORDER BY id LIMIT 200")]
