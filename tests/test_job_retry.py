from edgeops.domain.jobs import JobRequest
from tests.support import IsolatedCase


class RetryTests(IsolatedCase):
    def test_failure_backs_off_and_becomes_dead_letter(self):
        job_id = self.jobs.enqueue(JobRequest("events.query", '{"limit":999}', max_attempts=2))
        first = self.jobs.work_once()
        self.assertEqual((first["status"], first["attempts"], first["due_at"]), ("pending", 1, 1005))
        self.assertIsNone(self.jobs.work_once())
        self.now = 1005
        second = self.jobs.work_once()
        self.assertEqual((second["status"], second["attempts"]), ("dead", 2))
        self.assertEqual([run["status"] for run in second["runs"]], ["failed", "failed"])
        self.now += 10000
        self.assertIsNone(self.jobs.work_once())
