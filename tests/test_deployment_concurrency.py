"""Concurrent deployment writers cannot both advance the same revision."""
from concurrent.futures import ThreadPoolExecutor
from edgeops.application.deployments import DeploymentService
from edgeops.domain import Device
from tests.support import IsolatedCase

class ConcurrentDeploymentTests(IsolatedCase):
    def test_compare_and_swap_keeps_one_transition(self):
        self.operations.register_device(Device('a','A','sensor'))
        path=self.root/'firmware';path.write_bytes(b'x')
        service=DeploymentService(self.operations);artifact=service.register(path,'1.0.0');run=service.create('a',artifact['id'])
        def advance(_):
            try: return service.advance(run['id'],0,'start')['state']
            except ValueError: return 'stale'
        with ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(advance,range(2)))
        self.assertEqual(sorted(results),['stale','transferring'])
        self.assertEqual(len(service.get(run['id'])['history']),1)
