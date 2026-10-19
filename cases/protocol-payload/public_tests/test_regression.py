import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.devices.protocol import MAX_PAYLOAD
        self.assertEqual(MAX_PAYLOAD,4096)

if __name__ == "__main__": unittest.main()
