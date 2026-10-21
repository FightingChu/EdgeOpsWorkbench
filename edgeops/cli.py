"""Command-line entry point."""

import argparse
import json
import sys
import threading
import webbrowser

from .api import make_server
from .application import OperationsService
from .config import load_settings
from .devices import load_demo
from .domain.event_query import EventQuery
from . import cli_cases, cli_data, cli_jobs, cli_workflows
from . import cli_analytics, cli_alerts, cli_configuration, cli_interchange, cli_deployments


def parser():
    result = argparse.ArgumentParser(prog="edgeops", description="Local device operations workbench")
    result.add_argument("--config")
    result.add_argument("--data-dir")
    subcommands = result.add_subparsers(dest="command", required=True)
    subcommands.add_parser("init", help="initialize the database")
    subcommands.add_parser("demo", help="load deterministic demo data")
    subcommands.add_parser("summary", help="print current counts as JSON")
    cli_jobs.configure(subcommands)
    cli_data.configure(subcommands)
    cli_workflows.configure(subcommands)
    cli_cases.configure(subcommands)
    for extension in (cli_analytics,cli_alerts,cli_configuration,cli_interchange,cli_deployments):
        extension.configure(subcommands)
    ingest = subcommands.add_parser("import-events", help="atomically import a JSONL or text file")
    ingest.add_argument("path")
    ingest.add_argument("--format", choices=("jsonl", "text"), default="jsonl")
    ingest.add_argument("--encoding", default="utf-8")
    events = subcommands.add_parser("events", help="query a bounded page of events as JSON")
    events.add_argument("--limit", type=int, default=50)
    for name in ("cursor", "q", "severity", "service", "device-id", "since", "until"):
        events.add_argument("--" + name)
    serve = subcommands.add_parser("serve", help="start the local dashboard")
    serve.add_argument("--host")
    serve.add_argument("--port", type=int)
    serve.add_argument("--open", action="store_true")
    return result


def _run(argv=None):
    args = parser().parse_args(argv)
    settings = load_settings(args.config, host=getattr(args, "host", None),
                             port=getattr(args, "port", None), data_dir=args.data_dir)
    service = OperationsService(settings.database_path)
    if args.command == "init":
        service.initialize()
        print(settings.database_path.resolve())
    elif args.command == "demo":
        print(json.dumps(load_demo(service), ensure_ascii=False, indent=2))
    elif args.command == "summary":
        print(json.dumps(service.summary(), ensure_ascii=False, indent=2))
    elif args.command == "import-events":
        print(json.dumps(service.import_events(args.path, format=args.format, encoding=args.encoding),
                         ensure_ascii=False, indent=2))
    elif args.command == "events":
        query = EventQuery(**{name: getattr(args, name) for name in
                             ("limit", "cursor", "q", "severity", "service", "device_id", "since", "until")})
        print(json.dumps(service.list_events(query), ensure_ascii=False, indent=2))
    elif args.command in {"jobs", "schedules"}:
        print(json.dumps(cli_jobs.run(args, service), ensure_ascii=False, indent=2))
    elif args.command in {"diagnostics", "audit", "health-history", "backup", "verify-backup", "restore"}:
        print(json.dumps(cli_data.run(args, service), ensure_ascii=False, indent=2))
    elif args.command in {"workflows", "plugins"}:
        print(json.dumps(cli_workflows.run(args, service), ensure_ascii=False, indent=2))
    elif args.command == "cases":
        result = cli_cases.run(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.case_command == "verify" and not result["passed"]:
            return 1
    elif args.command in {"analytics","evaluate-rules","configuration","convert-events","export-events","deployments"}:
        handlers={"analytics":cli_analytics,"evaluate-rules":cli_alerts,"configuration":cli_configuration,"convert-events":cli_interchange,"export-events":cli_interchange,"deployments":cli_deployments}
        print(json.dumps(handlers[args.command].run(args,service),ensure_ascii=False,indent=2))
    elif args.command == "serve":
        server = make_server(settings)
        url = f"http://{settings.host}:{server.server_address[1]}"
        print(url)
        if args.open:
            threading.Timer(0.25, webbrowser.open, args=(url,)).start()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
    return 0


def main(argv=None):
    try:
        return _run(argv)
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"edgeops: {exc}", file=sys.stderr)
        return 2
