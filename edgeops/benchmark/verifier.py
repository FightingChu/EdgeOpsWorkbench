"""Behavior-based case checks run under the target's own module path."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

from .patches import load_fault
from .workspace import setup_case


def verify_case(case_directory, target, timeout=30):
    target = Path(target).resolve()
    if not (target / "edgeops").is_dir():
        raise ValueError("target is not an EdgeOps workspace")
    fault = load_fault(Path(case_directory) / "fault.json")
    target_case = target / "cases" / Path(case_directory).name
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(target_case / "public_tests"), "-v"],
                            cwd=target, capture_output=True, timeout=timeout)
    project = (target / "pyproject.toml").read_text(encoding="utf-8")
    no_dependencies = "dependencies = []" in project
    return {"passed": result.returncode == 0 and no_dependencies, "exit_code": result.returncode,
            "runtime_dependencies_empty": no_dependencies,
            "output": (result.stdout + result.stderr).decode("utf-8", errors="replace")[-16000:]}


def case_main(script, mode):
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    args = parser.parse_args()
    directory = Path(script).resolve().parent
    if mode == "setup":
        marker = setup_case(directory, args.target)
        print(json.dumps({"case_id": marker["case_id"], "target": marker["target"]}, indent=2))
        return 0
    result = verify_case(directory, args.target)
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1
