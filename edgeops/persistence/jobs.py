"""Serialized claims, expiring leases, and atomic completion evidence."""

import json
import uuid

from ..domain.jobs import backoff
from ..domain.validation import bounded_json, integer
from .audit import record
from .repositories import utc_now


def enqueue(connection, request):
    cursor = connection.execute(
        """INSERT INTO jobs(action,payload_json,due_at,max_attempts,retry_delay,dedup_key,status,created_at,updated_at)
           VALUES(?,?,?,?,?,?,'pending',?,?) ON CONFLICT(dedup_key) DO NOTHING""",
        (request.action, request.payload_json, request.due_at, request.max_attempts,
         request.retry_delay, request.dedup_key, utc_now(), utc_now()),
    )
    if cursor.rowcount:
        job_id = cursor.lastrowid
        record(connection, "job.enqueue", job_id, {"action": request.action})
        return job_id
    existing = connection.execute("SELECT * FROM jobs WHERE dedup_key=?", (request.dedup_key,)).fetchone()
    if any(existing[key] != getattr(request, key) for key in ("action", "payload_json", "due_at", "max_attempts", "retry_delay")):
        raise ValueError("dedup key already belongs to a different job request")
    return existing["id"]


def claim(connection, now, lease_seconds):
    integer(lease_seconds, "lease_seconds", 1, 3600)
    expired = connection.execute("SELECT * FROM jobs WHERE status='running' AND lease_until<=? ORDER BY id", (now,)).fetchall()
    for job in expired:
        status = "dead" if job["attempts"] >= job["max_attempts"] else "pending"
        connection.execute(
            "UPDATE jobs SET status=?,lease_token=NULL,lease_until=NULL,error='lease expired',updated_at=? WHERE id=?",
            (status, utc_now(), job["id"]),
        )
        connection.execute("UPDATE job_runs SET status='expired',finished_at=?,error='lease expired' WHERE lease_token=?", (now, job["lease_token"]))
        record(connection, "job.expire", job["id"], {"status": status})
    row = connection.execute(
        "SELECT * FROM jobs WHERE status='pending' AND due_at<=? ORDER BY due_at,id LIMIT 1", (now,)
    ).fetchone()
    if row is None:
        return None
    token = uuid.uuid4().hex
    attempt = row["attempts"] + 1
    connection.execute(
        "UPDATE jobs SET status='running',attempts=?,lease_token=?,lease_until=?,updated_at=? WHERE id=?",
        (attempt, token, now + lease_seconds, utc_now(), row["id"]),
    )
    connection.execute(
        "INSERT INTO job_runs(job_id,attempt,lease_token,started_at,status) VALUES(?,?,?,?,'running')",
        (row["id"], attempt, token, now),
    )
    record(connection, "job.claim", row["id"], {"attempt": attempt})
    return dict(connection.execute("SELECT * FROM jobs WHERE id=?", (row["id"],)).fetchone())


def finish(connection, job_id, token, now, *, result=None, error=None):
    row = connection.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    if row is None or row["status"] != "running" or row["lease_token"] != token or row["lease_until"] <= now:
        return False
    payload = bounded_json(result) if error is None else None
    status = "succeeded" if error is None else "dead" if row["attempts"] >= row["max_attempts"] else "pending"
    due_at = row["due_at"] if error is None else now + backoff(row["retry_delay"], row["attempts"])
    message = str(error)[:2048] if error is not None else None
    connection.execute(
        "UPDATE jobs SET status=?,due_at=?,result_json=?,error=?,lease_token=NULL,lease_until=NULL,updated_at=? WHERE id=?",
        (status, due_at, payload, message, utc_now(), job_id),
    )
    connection.execute("UPDATE job_runs SET status=?,finished_at=?,error=? WHERE lease_token=?",
                       ("succeeded" if error is None else "failed", now, message, token))
    if error is None and row["action"] == "health.snapshot":
        connection.execute("INSERT INTO health_snapshots(job_id,recorded_at,snapshot_json) VALUES(?,?,?)", (job_id, now, payload))
    record(connection, "job.finish", job_id, {"status": status, "error": message})
    return True


def cancel(connection, job_id, now):
    row = connection.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    if row is None:
        raise ValueError("job not found")
    if row["status"] not in {"pending", "running"}:
        return False
    connection.execute("UPDATE jobs SET status='cancelled',lease_token=NULL,lease_until=NULL,updated_at=? WHERE id=?", (utc_now(), job_id))
    if row["lease_token"]:
        connection.execute("UPDATE job_runs SET status='cancelled',finished_at=? WHERE lease_token=?", (now, row["lease_token"]))
    record(connection, "job.cancel", job_id, {})
    return True


def get(connection, job_id):
    row = connection.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    if row is None:
        return None
    item = dict(row)
    item.pop("lease_token")
    item["payload"] = json.loads(item.pop("payload_json"))
    raw = item.pop("result_json")
    item["result"] = json.loads(raw) if raw is not None else None
    item["runs"] = [dict(row) for row in connection.execute(
        "SELECT attempt,started_at,finished_at,status,error FROM job_runs WHERE job_id=? ORDER BY attempt", (job_id,)
    )]
    return item


def list_jobs(connection, limit=100):
    integer(limit, "limit", 1, 200)
    return [get(connection, row[0]) for row in connection.execute("SELECT id FROM jobs ORDER BY id DESC LIMIT ?", (limit,))]
