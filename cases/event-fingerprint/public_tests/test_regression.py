import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.domain.events import Event
        self.assertEqual(len(Event("x").fingerprint),64)

if __name__ == "__main__": unittest.main()
