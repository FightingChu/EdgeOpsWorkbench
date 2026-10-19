import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.config import Settings
        self.assertIn(Settings().host, {"127.0.0.1", "localhost"})

if __name__ == "__main__": unittest.main()
