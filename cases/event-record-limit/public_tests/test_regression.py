import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.application.event_import import MAX_RECORDS
        self.assertGreaterEqual(MAX_RECORDS,10000)

if __name__ == "__main__": unittest.main()
