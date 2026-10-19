from edgeops.domain.schedules import Schedule
from tests.support import IsolatedCase


class ScheduleTests(IsolatedCase):
    def test_bounded_catch_up_preserves_every_instant(self):
        self.jobs.add_schedule(Schedule("health", "health.snapshot", 10, 970))
        self.assertEqual(len(self.jobs.tick(limit=2)), 2)
        self.assertEqual(len(self.jobs.tick(limit=2)), 2)
        self.assertEqual(self.jobs.tick(), [])
        self.assertEqual(sorted(job["due_at"] for job in self.jobs.list()), [970, 980, 990, 1000])

    def test_disabled_schedule_preserves_cursor(self):
        schedule_id = self.jobs.add_schedule(Schedule("health", "health.snapshot", 10, 1000))
        self.jobs.enable_schedule(schedule_id, False)
        self.assertEqual(self.jobs.tick(), [])
        self.jobs.enable_schedule(schedule_id, True)
        self.assertEqual(len(self.jobs.tick()), 1)
