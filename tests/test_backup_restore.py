from edgeops.application import OperationsService
from edgeops.domain import Device
from edgeops.persistence.backup import create_backup, restore_backup, verify_backup
from tests.support import IsolatedCase


class BackupTests(IsolatedCase):
    def test_roundtrip_into_new_directory(self):
        self.operations.register_device(Device("设备", "海鸥", "sensor"))
        backup = self.root / "snapshot"
        manifest = create_backup(self.operations.database.path, backup)
        self.assertEqual(verify_backup(backup), manifest)
        restored = restore_backup(backup, self.root / "restored")
        self.assertEqual(OperationsService(restored).list_devices()[0]["name"], "海鸥")

    def test_existing_targets_are_never_overwritten(self):
        with self.assertRaisesRegex(ValueError, "must not exist"):
            create_backup(self.operations.database.path, self.root)
        backup = self.root / "snapshot"
        create_backup(self.operations.database.path, backup)
        with self.assertRaisesRegex(ValueError, "must not exist"):
            restore_backup(backup, self.root)
