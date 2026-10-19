import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from pathlib import Path
        self.assertTrue((Path("edgeops/static")/"sw.js").is_file())

if __name__ == "__main__": unittest.main()
