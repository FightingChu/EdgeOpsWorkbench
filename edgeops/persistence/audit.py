"""Transaction-local mutation evidence, bounded for operator queries."""

import json

from ..domain.validation import bounded_json, integer
from .repositories import utc_now


def record(connection, action, target, details):
    connection.execute(
        "INSERT INTO audit_entries(action,target,details_json,created_at) VALUES(?,?,?,?)",
        (action, str(target), bounded_json(details), utc_now()),
    )


def recent(connection, limit=100):
    integer(limit, "limit", 1, 200)
    rows = []
    for row in connection.execute("SELECT * FROM audit_entries ORDER BY id DESC LIMIT ?", (limit,)):
        item = dict(row)
        item["details"] = json.loads(item.pop("details_json"))
        rows.append(item)
    return rows
