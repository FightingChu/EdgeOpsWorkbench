import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.media.redaction import redact_metadata
        self.assertEqual(redact_metadata({"path":"C:\\secret"}),{})

if __name__ == "__main__": unittest.main()
