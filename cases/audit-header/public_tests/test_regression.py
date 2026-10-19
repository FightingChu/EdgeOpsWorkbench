import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.security import audit_headers
        self.assertFalse(audit_headers({"X-Frame-Options":"ALLOW"})[2].passed)

if __name__ == "__main__": unittest.main()
