from edgeops.persistence import workflows
from tests.support import IsolatedCase


class WorkflowLeaseTests(IsolatedCase):
    def test_expired_worker_cannot_commit_step(self):
        run_id = self.workflows.start(self.workflow())
        with self.operations.database.connect() as connection:
            old = workflows.claim(connection, run_id, self.now, 1)
        self.now += 1
        self.assertEqual(self.workflows.resume(run_id)["status"], "succeeded")
        with self.operations.database.connect() as connection:
            self.assertFalse(workflows.finish_step(connection, run_id, old, 0, self.now, result={}))

    def test_active_claim_blocks_second_worker(self):
        run_id = self.workflows.start(self.workflow())
        with self.operations.database.connect() as connection:
            workflows.claim(connection, run_id, self.now, 60)
        self.assertEqual(self.workflows.resume(run_id)["steps"], [])
