"""Source audit distinguishes executable implementation from count padding."""
import unittest
from scripts.source_audit import has_implementation,audit

class SourceAuditTests(unittest.TestCase):
    def test_empty_import_only_and_constant_return_do_not_count(self):
        for source in ('','import os','def f(): pass','def f(): return None','def f(): raise NotImplementedError'):
            with self.subTest(source=source): self.assertFalse(has_implementation(source))
    def test_branch_and_computation_count(self):
        self.assertTrue(has_implementation('def f(value): return value + 1'))
        self.assertTrue(has_implementation('class C:'+chr(10)+'    def f(self, values): return [x*2 for x in values]'))
    def test_repository_sources_parse(self):
        report=audit(include_untracked=True)
        self.assertEqual(report['syntax_errors'],[])
        self.assertGreaterEqual(report['valid_python_without_cases'],300)
