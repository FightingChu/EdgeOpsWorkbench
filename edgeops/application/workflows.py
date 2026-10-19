"""Dry-run validation and restartable, side-effect-free workflow actions."""

import json
import time

from ..domain.event_query import EventQuery
from ..domain.validation import bounded_json, clock_value, integer
from ..domain.workflows import resolve, validate_workflow
from ..persistence import workflows
from ..plugins import PluginHost


class WorkflowService:
    def __init__(self, operations, plugins=None, clock=time.time):
        self.operations = operations
        self.database = operations.database
        self.plugins = plugins if plugins is not None else PluginHost()
        self.clock = clock

    def dry_run(self, definition):
        definition = validate_workflow(definition)
        return {"valid": True, "name": definition["name"], "steps": [step["id"] for step in definition["steps"]]}

    def start(self, definition, inputs=None):
        validate_workflow(definition)
        inputs = {} if inputs is None else inputs
        if not isinstance(inputs, dict):
            raise ValueError("workflow input must be an object")
        bounded_json(inputs)
        self.database.initialize()
        with self.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            return workflows.create(connection, definition, inputs)

    def get(self, run_id):
        self.database.initialize()
        with self.database.connect() as connection:
            return workflows.get(connection, run_id)

    def cancel(self, run_id):
        self.database.initialize()
        with self.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            return workflows.cancel(connection, run_id)

    def _execute(self, action, params):
        if action == "emit":
            return params
        if action == "assert.equal":
            if set(params) != {"actual", "expected"} or params["actual"] != params["expected"]:
                raise ValueError("workflow equality assertion failed")
            return {"matched": True}
        if action == "summary":
            if params:
                raise ValueError("summary accepts no parameters")
            return self.operations.summary()
        if action == "events.query":
            return self.operations.list_events(EventQuery(**params))
        if action == "plugin.invoke":
            if set(params) != {"name", "request"}:
                raise ValueError("plugin action requires name and request")
            return self.plugins.invoke(params["name"], params["request"])
        raise ValueError("unsupported workflow action")

    def resume(self, run_id, *, max_steps=50, lease_seconds=60):
        integer(max_steps, "max_steps", 1, 50)
        integer(lease_seconds, "lease_seconds", 1, 3600)
        self.database.initialize()
        for _ in range(max_steps):
            with self.database.connect() as connection:
                connection.execute("BEGIN IMMEDIATE")
                token = workflows.claim(connection, run_id, clock_value(self.clock()), lease_seconds)
                run = workflows.get(connection, run_id)
            if token is None:
                return run
            position = run["current_step"]
            step = run["definition"]["steps"][position]
            context = {"input": run["input"], "steps": {item["step_id"]: item["result"] for item in run["steps"] if item["status"] == "succeeded"}}
            result = error = None
            try:
                result = self._execute(step["action"], resolve(step["params"], context))
                bounded_json(result)
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"
            with self.database.connect() as connection:
                connection.execute("BEGIN IMMEDIATE")
                accepted = workflows.finish_step(connection, run_id, token, position, clock_value(self.clock()), result=result, error=error)
                run = workflows.get(connection, run_id)
            if not accepted or run["status"] in {"failed", "cancelled", "succeeded"}:
                return run
        return self.get(run_id)
