import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.domain.workflows import validate_workflow
        with self.assertRaises(ValueError): validate_workflow({"version":1,"name":"x","steps":[{"id":"a","action":"emit","params":{}}]})

if __name__ == "__main__": unittest.main()
