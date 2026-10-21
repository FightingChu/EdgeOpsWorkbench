"""Database-backed numeric reports keep device series separate."""
from datetime import datetime,timezone
from edgeops.application.analytics import AnalyticsService
from edgeops.devices import load_demo
from tests.support import IsolatedCase

class AnalyticsServiceTests(IsolatedCase):
    def test_device_series_do_not_mix(self):
        load_demo(self.operations,datetime(2026,10,21,tzinfo=timezone.utc))
        report=AnalyticsService(self.operations).report('temperature')
        by_device={row['device_id']:row for row in report['series']}
        self.assertEqual(report['count'],3)
        self.assertEqual(by_device['press-01']['statistics']['mean'],73)
        self.assertEqual(by_device['camera-01']['statistics']['count'],1)
    def test_empty_series_is_explicit(self):
        self.assertEqual(AnalyticsService(self.operations).report('missing')['series'],[])
    def test_limit_and_identity_are_bounded(self):
        service=AnalyticsService(self.operations)
        with self.assertRaises(ValueError): service.report('temperature',limit=10001)
        with self.assertRaises(ValueError): service.readings('bad'+chr(10)+'metric')
