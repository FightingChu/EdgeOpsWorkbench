import unittest
from edgeops.configuration.endpoints import local_endpoint

class LocalEndpointTests(unittest.TestCase):
    def test_loopback_endpoint(self):
        self.assertEqual(local_endpoint('http://127.0.0.1:8877/api'),'http://127.0.0.1:8877/api')
    def test_external_and_credentials_rejected(self):
        for url in ('http://example.com:80','http://u:p@localhost:80','http://localhost:80/#x'):
            with self.assertRaises(ValueError): local_endpoint(url)
