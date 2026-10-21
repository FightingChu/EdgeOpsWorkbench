import unittest
from edgeops.domain.deployment.chunks import split,assemble

class FirmwareChunkTests(unittest.TestCase):
    def test_chunk_roundtrip(self):
        self.assertEqual(assemble(split(b'abcdefgh',3),8),b'abcdefgh')
    def test_missing_and_tampered_chunk_rejected(self):
        chunks=split(b'abcd',2)
        with self.assertRaises(ValueError): assemble(chunks[1:],4)
        chunks[0]['data']=b'xx'
        with self.assertRaises(ValueError): assemble(chunks,4)
