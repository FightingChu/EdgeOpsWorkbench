from edgeops.persistence import workflows
from tests.support import IsolatedCase


class WorkflowCancelTests(IsolatedCase):
    def test_cancel_blocks_inflight_and_future_commits(self):
        run_id = self.workflows.start(self.workflow())
        with self.operations.database.connect() as connection:
            token = workflows.claim(connection, run_id, self.now, 60)
        self.assertTrue(self.workflows.cancel(run_id))
        with self.operations.database.connect() as connection:
            self.assertFalse(workflows.finish_step(connection, run_id, token, 0, self.now, result={}))
        self.assertEqual(self.workflows.resume(run_id)["status"], "cancelled")

    def test_cancelling_completed_workflow_is_noop(self):
        run_id = self.workflows.start(self.workflow())
        self.workflows.resume(run_id)
        self.assertFalse(self.workflows.cancel(run_id))
