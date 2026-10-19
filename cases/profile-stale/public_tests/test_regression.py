import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.clients.profiles import get_profile
        self.assertEqual(get_profile("local").stale_write_policy,"reject")

if __name__ == "__main__": unittest.main()
