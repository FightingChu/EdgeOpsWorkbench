"""Deployment transition and audit failures roll back revision and history together."""
import sqlite3
from edgeops.application.deployments import DeploymentService
from edgeops.domain import Device
from tests.support import IsolatedCase

class DeploymentTransactionTests(IsolatedCase):
    def test_audit_failure_rolls_back_transition(self):
        self.operations.register_device(Device('a','A','sensor'));path=self.root/'fw';path.write_bytes(b'x')
        service=DeploymentService(self.operations);artifact=service.register(path,'1.0.0');run=service.create('a',artifact['id'])
        with self.operations.database.connect() as connection:
            connection.execute("CREATE TRIGGER reject_deployment_audit BEFORE INSERT ON audit_entries WHEN NEW.action='deployment.transition' BEGIN SELECT RAISE(ABORT,'injected'); END")
        with self.assertRaises(sqlite3.IntegrityError): service.advance(run['id'],0,'start')
        unchanged=service.get(run['id']);self.assertEqual((unchanged['revision'],unchanged['state']),(0,'queued'));self.assertEqual(unchanged['history'],[])
