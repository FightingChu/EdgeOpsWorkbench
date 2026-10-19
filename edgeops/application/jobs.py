"""Clock-injected durable task orchestration without background sleeps."""

import json
import time

from ..domain.jobs import JobRequest
from ..domain.schedules import Schedule
from ..domain.validation import clock_value
from ..persistence import jobs, schedules
from .actions import ACTIONS, execute


class JobService:
    def __init__(self, operations, clock=time.time):
        self.operations = operations
        self.database = operations.database
        self.clock = clock

    def enqueue(self, request):
        if not isinstance(request, JobRequest) or request.action not in ACTIONS:
            raise ValueError("unsupported job request")
        self.database.initialize()
        with self.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            return jobs.enqueue(connection, request)

    def work_once(self, lease_seconds=60):
        now = clock_value(self.clock())
        self.database.initialize()
        with self.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            job = jobs.claim(connection, now, lease_seconds)
        if job is None:
            return None
        result = error = None
        try:
            result = execute(self.operations, job["action"], json.loads(job["payload_json"]))
            from ..domain.validation import bounded_json
            bounded_json(result)
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
        with self.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            jobs.finish(connection, job["id"], job["lease_token"], clock_value(self.clock()), result=result, error=error)
            return jobs.get(connection, job["id"])

    def cancel(self, job_id):
        self.database.initialize()
        with self.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            return jobs.cancel(connection, job_id, clock_value(self.clock()))

    def get(self, job_id):
        self.database.initialize()
        with self.database.connect() as connection:
            return jobs.get(connection, job_id)

    def list(self, limit=100):
        self.database.initialize()
        with self.database.connect() as connection:
            return jobs.list_jobs(connection, limit)

    def add_schedule(self, schedule):
        if not isinstance(schedule, Schedule) or schedule.action not in ACTIONS:
            raise ValueError("unsupported schedule action")
        self.database.initialize()
        with self.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            return schedules.create(connection, schedule)

    def tick(self, limit=100):
        self.database.initialize()
        with self.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            return schedules.dispatch(connection, clock_value(self.clock()), limit)

    def schedules(self):
        self.database.initialize()
        with self.database.connect() as connection:
            return schedules.list_schedules(connection)

    def enable_schedule(self, schedule_id, enabled):
        self.database.initialize()
        with self.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            schedules.set_enabled(connection, schedule_id, enabled)
