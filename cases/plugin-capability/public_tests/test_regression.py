import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.domain.plugins import PluginManifest
        with self.assertRaises(ValueError): PluginManifest.parse({"version":1,"name":"x","kind":"importer","entrypoint":"x.py:run","capabilities":["events.decode"],"description":"x"})

if __name__ == "__main__": unittest.main()
