import json

from edgeops.persistence.backup import create_backup, verify_backup, file_hash
from tests.support import IsolatedCase


class BackupCorruptionTests(IsolatedCase):
    def test_truncation_detected_by_hash(self):
        backup = self.root / "snapshot"
        create_backup(self.operations.database.path, backup)
        path = backup / "edgeops.sqlite3"
        path.write_bytes(path.read_bytes()[:100])
        with self.assertRaisesRegex(ValueError, "mismatch"):
            verify_backup(backup)

    def test_manifest_schema_mismatch_rejected(self):
        backup = self.root / "snapshot"
        manifest = create_backup(self.operations.database.path, backup)
        manifest["schema_version"] = 1
        (backup / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "schema mismatch"):
            verify_backup(backup)
