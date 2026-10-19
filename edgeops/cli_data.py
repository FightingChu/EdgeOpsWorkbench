"""Explicit non-destructive backup and diagnostic commands."""

from .application.diagnostics import DiagnosticsService
from .persistence.backup import create_backup, restore_backup, verify_backup


def configure(subcommands):
    for command, help_text in (("diagnostics", "inspect database without migrating"),
                               ("audit", "read recent mutation evidence"),
                               ("health-history", "read durable service snapshots")):
        subcommands.add_parser(command, help=help_text)
    backup = subcommands.add_parser("backup", help="snapshot into a new directory")
    backup.add_argument("destination")
    verify = subcommands.add_parser("verify-backup", help="verify backup hash, schema, and integrity")
    verify.add_argument("directory")
    restore = subcommands.add_parser("restore", help="restore into a new directory")
    restore.add_argument("directory")
    restore.add_argument("destination")


def run(args, operations):
    if args.command == "backup":
        return create_backup(operations.database.path, args.destination)
    if args.command == "verify-backup":
        return verify_backup(args.directory)
    if args.command == "restore":
        return {"database": restore_backup(args.directory, args.destination)}
    service = DiagnosticsService(operations)
    return {"diagnostics": service.report, "audit": service.audit,
            "health-history": service.health_history}[args.command]()
