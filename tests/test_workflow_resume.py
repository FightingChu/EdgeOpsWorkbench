from tests.support import IsolatedCase


class ResumeTests(IsolatedCase):
    def test_resume_from_durable_step_without_repeating_previous_action(self):
        run_id = self.workflows.start(self.workflow())
        first = self.workflows.resume(run_id, max_steps=1)
        self.assertEqual(first["status"], "pending")
        final = self.workflows.resume(run_id)
        self.assertEqual(final["status"], "succeeded")
        self.assertEqual([step["attempts"] for step in final["steps"]], [1, 1])
        self.assertEqual(self.workflows.resume(run_id)["steps"], final["steps"])

    def test_failed_reference_preserves_completed_step(self):
        definition = self.workflow()
        definition["steps"][1]["params"]["actual"] = {"$ref": "steps.first.missing"}
        run_id = self.workflows.start(definition)
        result = self.workflows.resume(run_id)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["current_step"], 1)
        result = self.workflows.resume(run_id)
        self.assertEqual([step["attempts"] for step in result["steps"]], [1, 2])
