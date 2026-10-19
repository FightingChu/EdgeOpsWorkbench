from edgeops.domain.jobs import JobRequest
from edgeops.persistence import jobs
from tests.support import IsolatedCase


class CancelTests(IsolatedCase):
    def test_cancel_pending_prevents_claim(self):
        job_id = self.jobs.enqueue(JobRequest("health.snapshot"))
        self.assertTrue(self.jobs.cancel(job_id))
        self.assertFalse(self.jobs.cancel(job_id))
        self.assertIsNone(self.jobs.work_once())

    def test_cancel_inflight_prevents_commit(self):
        job_id = self.jobs.enqueue(JobRequest("health.snapshot"))
        with self.operations.database.connect() as connection:
            job = jobs.claim(connection, self.now, 60)
        self.jobs.cancel(job_id)
        with self.operations.database.connect() as connection:
            self.assertFalse(jobs.finish(connection, job_id, job["lease_token"], self.now, result={}))
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM health_snapshots").fetchone()[0], 0)
