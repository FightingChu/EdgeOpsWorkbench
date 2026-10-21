import unittest
from edgeops.codecs.cloudevents import decode,encode

class CloudEventTests(unittest.TestCase):
    def test_envelope_identity_is_retained(self):
        result=decode(encode({'message':'x'},'id1','edge/site','device.log'))
        self.assertEqual(result['metadata']['cloud_event']['id'],'id1')
    def test_unsupported_version_rejected(self):
        with self.assertRaises(ValueError): decode('{"specversion":"0.3"}')
