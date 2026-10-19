"""Workflow leases keep retries and cancellation from committing stale results."""

import json
import uuid

from ..domain.validation import bounded_json
from .audit import record
from .repositories import utc_now


def create(connection, definition, inputs):
    cursor = connection.execute(
        "INSERT INTO workflow_runs(definition_json,input_json,status,created_at,updated_at) VALUES(?,?,'pending',?,?)",
        (bounded_json(definition), bounded_json(inputs), utc_now(), utc_now()),
    )
    record(connection, "workflow.create", cursor.lastrowid, {"name": definition["name"]})
    return cursor.lastrowid


def get(connection, run_id):
    row = connection.execute("SELECT * FROM workflow_runs WHERE id=?", (run_id,)).fetchone()
    if row is None:
        return None
    run = dict(row)
    run["definition"] = json.loads(run.pop("definition_json"))
    run["input"] = json.loads(run.pop("input_json"))
    run.pop("lease_token")
    run["steps"] = []
    for row in connection.execute("SELECT * FROM workflow_steps WHERE run_id=? ORDER BY position", (run_id,)):
        step = dict(row)
        raw = step.pop("result_json")
        step["result"] = json.loads(raw) if raw is not None else None
        run["steps"].append(step)
    return run


def claim(connection, run_id, now, lease_seconds):
    row = connection.execute("SELECT * FROM workflow_runs WHERE id=?", (run_id,)).fetchone()
    if row is None:
        raise ValueError("workflow run not found")
    if row["status"] in {"succeeded", "cancelled"} or (row["status"] == "running" and row["lease_until"] > now):
        return None
    token = uuid.uuid4().hex
    connection.execute("UPDATE workflow_runs SET status='running',lease_token=?,lease_until=?,error=NULL,updated_at=? WHERE id=?", (token, now + lease_seconds, utc_now(), run_id))
    record(connection, "workflow.claim", run_id, {"position": row["current_step"]})
    return token


def finish_step(connection, run_id, token, position, now, *, result=None, error=None):
    row = connection.execute("SELECT * FROM workflow_runs WHERE id=?", (run_id,)).fetchone()
    if row is None or row["status"] != "running" or row["lease_token"] != token or row["lease_until"] <= now or row["current_step"] != position:
        return False
    definition = json.loads(row["definition_json"])
    step = definition["steps"][position]
    message = str(error)[:2048] if error is not None else None
    payload = bounded_json(result) if error is None else None
    connection.execute(
        """INSERT INTO workflow_steps(run_id,step_id,position,status,attempts,result_json,error)
           VALUES(?,?,?,?,1,?,?) ON CONFLICT(run_id,position) DO UPDATE SET
           status=excluded.status,attempts=workflow_steps.attempts+1,result_json=excluded.result_json,error=excluded.error""",
        (run_id, step["id"], position, "failed" if error is not None else "succeeded", payload, message),
    )
    next_step = position + (error is None)
    status = "failed" if error is not None else "succeeded" if next_step == len(definition["steps"]) else "pending"
    connection.execute("UPDATE workflow_runs SET status=?,current_step=?,error=?,lease_token=NULL,lease_until=NULL,updated_at=? WHERE id=?", (status, next_step, message, utc_now(), run_id))
    record(connection, "workflow.step", run_id, {"step": step["id"], "status": status, "error": message})
    return True


def cancel(connection, run_id):
    row = connection.execute("SELECT status FROM workflow_runs WHERE id=?", (run_id,)).fetchone()
    if row is None:
        raise ValueError("workflow run not found")
    if row[0] in {"succeeded", "cancelled"}:
        return False
    connection.execute("UPDATE workflow_runs SET status='cancelled',lease_token=NULL,lease_until=NULL,updated_at=? WHERE id=?", (utc_now(), run_id))
    record(connection, "workflow.cancel", run_id, {})
    return True
