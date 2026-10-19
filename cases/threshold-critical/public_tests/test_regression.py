import unittest

class RegressionTest(unittest.TestCase):
    def test_contract(self):
        from edgeops.domain import TelemetryReading, evaluate_reading
        from datetime import datetime, timezone
        r=TelemetryReading("d","temperature",85,"C",datetime.now(timezone.utc).isoformat())
        self.assertEqual(evaluate_reading(r).severity,"critical")

if __name__ == "__main__": unittest.main()
