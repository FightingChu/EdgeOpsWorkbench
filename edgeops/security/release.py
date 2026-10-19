"""Release gate summary for local reproducible archives."""


def release_gate(*, tests_passed, verification_passed, dependencies_empty, generated_excluded, findings=None):
    checks = {"tests": bool(tests_passed), "verification": bool(verification_passed), "dependencies": bool(dependencies_empty), "generated_excluded": bool(generated_excluded)}
    if findings:
        checks["critical_findings"] = not any(item.severity == "critical" and not item.passed for item in findings)
    return {"passed": all(checks.values()), "checks": checks}
