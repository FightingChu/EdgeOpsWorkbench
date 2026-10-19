from edgeops.domain.jobs import JobRequest
from edgeops.persistence import jobs
from tests.support import IsolatedCase


class LeaseTests(IsolatedCase):
    def test_restart_reclaims_expired_job_and_rejects_stale_result(self):
        job_id = self.jobs.enqueue(JobRequest("health.snapshot"))
        with self.operations.database.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            old = jobs.claim(connection, self.now, 10)
        self.now += 10
        result = self.jobs.work_once()
        self.assertEqual((result["id"], result["attempts"], result["status"]), (job_id, 2, "succeeded"))
        with self.operations.database.connect() as connection:
            self.assertFalse(jobs.finish(connection, job_id, old["lease_token"], self.now, result={}))
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM health_snapshots").fetchone()[0], 1)

    def test_expired_final_attempt_is_dead(self):
        job_id = self.jobs.enqueue(JobRequest("health.snapshot", max_attempts=1))
        with self.operations.database.connect() as connection:
            jobs.claim(connection, self.now, 1)
        self.now += 1
        self.assertIsNone(self.jobs.work_once())
        self.assertEqual(self.jobs.get(job_id)["status"], "dead")
