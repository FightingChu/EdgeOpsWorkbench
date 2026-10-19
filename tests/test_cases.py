from pathlib import Path
import tempfile
import unittest

from edgeops.benchmark import list_cases
from edgeops.benchmark.patches import load_fault
from edgeops.benchmark.workspace import setup_case, reset_case


class CaseTests(unittest.TestCase):
    def test_catalog_has_complete_bundles_and_exact_faults(self):
        root = Path(__file__).resolve().parents[1]
        cases = list_cases(root)
        self.assertEqual(len(cases), 18)
        for case in cases:
            fault = load_fault(root / "cases" / case["id"] / "fault.json")
            content = (root / fault["file"]).read_text(encoding="utf-8")
            self.assertEqual(content.count(fault["old"]), 1, case["id"])

    def test_setup_and_reset_require_a_disposable_target(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix="edgeops-case-test-") as temporary:
            target = Path(temporary) / "copy"
            marker = setup_case(root / "cases" / "local-bind", target, source=root)
            self.assertEqual(marker["case_id"], "local-bind")
            self.assertTrue((target / ".edgeops-case.json").is_file())
            reset_case(target, source=root)
            self.assertFalse(target.exists())
