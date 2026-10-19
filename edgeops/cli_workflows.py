"""Workflow and explicit trusted-plugin command adapters."""

import json
from pathlib import Path

from .application.workflows import WorkflowService
from .plugins import PluginHost


def read_json(path):
    path = Path(path)
    if path.stat().st_size > 65536:
        raise ValueError("JSON definition exceeds 65536 bytes")
    return json.loads(path.read_text(encoding="utf-8"))


def configure(subcommands):
    workflow = subcommands.add_parser("workflows", help="validate and execute resumable workflows")
    commands = workflow.add_subparsers(dest="workflow_command", required=True)
    for name in ("dry-run", "start"):
        command = commands.add_parser(name)
        command.add_argument("definition")
        if name == "start":
            command.add_argument("--input", default="{}")
    resume = commands.add_parser("resume")
    resume.add_argument("id", type=int)
    resume.add_argument("--max-steps", type=int, default=50)
    resume.add_argument("--plugin", action="append", default=[])
    for name in ("get", "cancel"):
        command = commands.add_parser(name)
        command.add_argument("id", type=int)
    plugins = subcommands.add_parser("plugins", help="inspect or invoke an explicitly selected plugin")
    plugins.add_argument("directory")
    plugins.add_argument("--request", help="JSON request; omit to inspect manifest")


def run(args, operations):
    host = PluginHost()
    if args.command == "plugins":
        manifest = host.load(args.directory)
        return manifest if args.request is None else host.invoke(manifest["name"], json.loads(args.request))
    for directory in getattr(args, "plugin", []):
        host.load(directory)
    service = WorkflowService(operations, plugins=host)
    command = args.workflow_command
    if command == "dry-run":
        return service.dry_run(read_json(args.definition))
    if command == "start":
        return {"run_id": service.start(read_json(args.definition), json.loads(args.input))}
    if command == "resume":
        return service.resume(args.id, max_steps=args.max_steps)
    if command == "get":
        return service.get(args.id)
    return {"cancelled": service.cancel(args.id)}
