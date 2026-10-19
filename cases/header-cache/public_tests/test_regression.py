import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.security import audit_headers
        self.assertTrue(audit_headers({"Cache-Control":"no-store","X-Content-Type-Options":"nosniff","X-Frame-Options":"DENY","Referrer-Policy":"no-referrer"})[0].passed)

if __name__ == "__main__": unittest.main()
