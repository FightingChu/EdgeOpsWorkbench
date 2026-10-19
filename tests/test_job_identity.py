from edgeops.domain.jobs import JobRequest
from tests.support import IsolatedCase


class JobIdentityTests(IsolatedCase):
    def test_dedup_key_is_idempotent_and_rejects_different_request(self):
        request = JobRequest("health.snapshot", dedup_key="operator-check-1")
        first = self.jobs.enqueue(request)
        self.assertEqual(self.jobs.enqueue(request), first)
        with self.assertRaisesRegex(ValueError, "different"):
            self.jobs.enqueue(JobRequest("devices.snapshot", dedup_key="operator-check-1"))
        self.assertEqual(len(self.jobs.list()), 1)

    def test_due_time_prevents_early_execution(self):
        self.jobs.enqueue(JobRequest("health.snapshot", due_at=1001))
        self.assertIsNone(self.jobs.work_once())
        self.now = 1001
        self.assertEqual(self.jobs.work_once()["status"], "succeeded")
