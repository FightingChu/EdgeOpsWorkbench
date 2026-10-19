import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.persistence.migrations import SCHEMA_VERSION
        self.assertEqual(SCHEMA_VERSION,4)

if __name__ == "__main__": unittest.main()
