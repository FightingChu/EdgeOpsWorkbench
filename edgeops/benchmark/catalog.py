"""Discover only complete benchmark bundles, with no product mutations."""

from pathlib import Path

from .manifest import read_manifest


ROOT = Path(__file__).resolve().parents[2]


def list_cases(root=ROOT):
    result = []
    for path in sorted((Path(root) / "cases").glob("*/manifest.json")):
        if path.parent.name == "templates":
            continue
        manifest = read_manifest(path)
        if manifest["id"] != path.parent.name:
            raise ValueError("case id does not match directory")
        for name in ("setup.py", "verify.py", "rounds.md", "fault.json", "public_tests/test_regression.py"):
            if not (path.parent / name).is_file():
                raise ValueError("incomplete case bundle: " + manifest["id"])
        result.append(manifest)
    return result
