from concurrent.futures import ThreadPoolExecutor

from edgeops.domain.jobs import JobRequest
from tests.support import IsolatedCase


class ConcurrentWorkerTests(IsolatedCase):
    def test_two_workers_commit_one_snapshot(self):
        self.jobs.enqueue(JobRequest("health.snapshot"))
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(lambda _: self.jobs.work_once(), range(2)))
        self.assertEqual(sum(result is not None for result in results), 1)
        with self.operations.database.connect() as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM health_snapshots").fetchone()[0], 1)
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM job_runs").fetchone()[0], 1)
