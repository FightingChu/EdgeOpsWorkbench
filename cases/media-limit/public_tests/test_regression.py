import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.media.evidence import MAX_MEDIA_BYTES
        self.assertGreaterEqual(MAX_MEDIA_BYTES,16*1024*1024)

if __name__ == "__main__": unittest.main()
