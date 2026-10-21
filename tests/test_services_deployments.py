"""Durable rollouts reject stale revisions and never mark failed simulation successful."""
from edgeops.application.deployments import DeploymentService
from edgeops.domain import Device
from tests.support import IsolatedCase

class DeploymentServiceTests(IsolatedCase):
    def prepare(self):
        self.operations.register_device(Device('sensor','Sensor','sensor'))
        path=self.root/'firmware.bin';path.write_bytes(b'firmware')
        service=DeploymentService(self.operations);artifact=service.register(path,'2.0.0')
        deployment=service.create('sensor',artifact['id'])
        return service,path,deployment
    def test_success_persists_verified_transition_history(self):
        service,path,deployment=self.prepare()
        result=service.run_simulation(deployment['id'],path)
        self.assertEqual(result['state'],'succeeded')
        self.assertEqual([row['action'] for row in result['history']],['start','transferred','verified','applied'])
        self.assertEqual(result['received_bytes'],8)
    def test_failed_simulation_keeps_failure_state(self):
        service,path,deployment=self.prepare()
        self.assertEqual(service.run_simulation(deployment['id'],path,'verify')['state'],'failed')
    def test_stale_writer_and_incomplete_transfer_rejected(self):
        service,path,deployment=self.prepare(); current=service.advance(deployment['id'],0,'start')
        with self.assertRaises(ValueError): service.advance(deployment['id'],0,'cancel')
        with self.assertRaises(ValueError): service.advance(deployment['id'],1,'transferred',received_bytes=1)
        self.assertEqual(service.get(deployment['id'])['revision'],1)
    def test_artifact_version_cannot_change_content(self):
        service,path,deployment=self.prepare();path.write_bytes(b'changed')
        with self.assertRaises(ValueError): service.register(path,'2.0.0')
    def test_unknown_device_cannot_start_rollout(self):
        service,path,deployment=self.prepare()
        with self.assertRaises(ValueError): service.create('missing',deployment['artifact_id'])
