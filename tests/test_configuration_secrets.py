import unittest
from edgeops.configuration.secrets import redact

class SecretRedactionTests(unittest.TestCase):
    def test_nested_secrets_are_not_exposed(self):
        self.assertEqual(redact({'api':{'access_token':'x','port':1}}),{'api':{'access_token':'<redacted>','port':1}})
    def test_arrays_are_traversed(self):
        self.assertEqual(redact([{'Password':'x'}]),[{'Password':'<redacted>'}])
