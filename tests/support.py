"""Shared isolated databases and injected clocks for reliability regressions."""

from pathlib import Path
import tempfile
import unittest

from edgeops.application import OperationsService
from edgeops.application.jobs import JobService
from edgeops.application.workflows import WorkflowService


ROOT = Path(__file__).resolve().parents[1]


class IsolatedCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="edgeops-test-")
        self.root = Path(self.temporary.name)
        self.now = 1000.0
        self.operations = OperationsService(self.root / "db.sqlite3")
        self.operations.initialize()
        self.jobs = JobService(self.operations, clock=lambda: self.now)
        self.workflows = WorkflowService(self.operations, clock=lambda: self.now)

    def tearDown(self):
        self.temporary.cleanup()

    def workflow(self, steps=None):
        return {"version": 1, "name": "regression", "steps": steps or [
            {"id": "first", "action": "emit", "params": {"value": 42}},
            {"id": "check", "action": "assert.equal", "params": {"actual": {"$ref": "steps.first.value"}, "expected": 42}},
        ]}
