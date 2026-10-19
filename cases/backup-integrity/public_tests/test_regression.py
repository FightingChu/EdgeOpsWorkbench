import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.domain.backup import validate_manifest
        with self.assertRaises(ValueError): validate_manifest({"version":1,"schema_version":1,"sha256":"x","bytes":1,"created_at":"2026-10-19T00:00:00Z","database":"edgeops.sqlite3"})

if __name__ == "__main__": unittest.main()
