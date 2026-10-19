import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.domain.jobs import backoff
        self.assertEqual(backoff(5,10),2560)

if __name__ == "__main__": unittest.main()
