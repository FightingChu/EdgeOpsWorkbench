import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.application.event_import import ENCODINGS
        self.assertIn("gb18030",ENCODINGS)

if __name__ == "__main__": unittest.main()
