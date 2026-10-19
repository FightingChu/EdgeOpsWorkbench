from pathlib import Path
import tempfile
import unittest

from edgeops.media import inspect_file, ingest_file
from edgeops.media.manifest import build_manifest
from edgeops.media.metadata import ImageMetadata
from edgeops.media.redaction import redact_metadata
from edgeops.media.storage import evidence_path
from edgeops.media.thumbnail import thumbnail_plan


class MediaTests(unittest.TestCase):
    def test_hash_copy_manifest_and_thumbnail_are_deterministic(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root); source = root / "sample.txt"; source.write_text("证据", encoding="utf-8")
            evidence = inspect_file(source)
            copied = ingest_file(source, root / "copy.txt")
            self.assertEqual(evidence.sha256, copied.sha256)
            manifest = build_manifest(evidence, {"token": "abc", "operator": "海鸥"})
            self.assertEqual(manifest["metadata"], {"operator": "海鸥"})
            self.assertEqual(thumbnail_plan(ImageMetadata(1920, 1080)), {"width": 320, "height": 180, "required": True})
            self.assertTrue(evidence_path(root, evidence.sha256, evidence.name).parent.name == evidence.sha256[:2])

    def test_rejects_unsupported_or_traversal_inputs(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "x.exe"; path.write_bytes(b"x")
            with self.assertRaises(ValueError): inspect_file(path)
        with self.assertRaises(ValueError): evidence_path(".", "0" * 64, "../escape")

