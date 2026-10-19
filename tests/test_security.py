import unittest

from edgeops.config import Settings
from edgeops.security import audit_headers, audit_settings, redact_report
from edgeops.security.release import release_gate


class SecurityTests(unittest.TestCase):
    def test_local_settings_and_headers_pass(self):
        findings = audit_settings(Settings()) + audit_headers({"Cache-Control": "no-store", "X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY", "Referrer-Policy": "no-referrer"})
        self.assertTrue(all(item.passed for item in findings))
        self.assertTrue(release_gate(tests_passed=True, verification_passed=True, dependencies_empty=True, generated_excluded=True, findings=findings)["passed"])

    def test_report_redacts_context(self):
        report = redact_report([], {"api_key": "secret", "path": "C:\\Users\\operator\\db"})
        self.assertEqual(report["context"], {})
