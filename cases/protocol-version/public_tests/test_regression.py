import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.devices.protocol import negotiate
        self.assertEqual(negotiate([1],["reading"])["version"],1)

if __name__ == "__main__": unittest.main()
