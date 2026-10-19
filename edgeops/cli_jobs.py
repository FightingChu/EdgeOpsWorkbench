"""CLI adapters for bounded job workers and explicit periodic dispatch."""

import json

from .application.jobs import JobService
from .domain.jobs import JobRequest
from .domain.schedules import Schedule


def configure(subcommands):
    jobs = subcommands.add_parser("jobs", help="enqueue, run, inspect, or cancel durable checks")
    commands = jobs.add_subparsers(dest="job_command", required=True)
    enqueue = commands.add_parser("enqueue")
    enqueue.add_argument("action")
    enqueue.add_argument("--payload", default="{}")
    enqueue.add_argument("--due-at", type=float, default=0)
    enqueue.add_argument("--max-attempts", type=int, default=3)
    enqueue.add_argument("--retry-delay", type=int, default=5)
    enqueue.add_argument("--dedup-key")
    commands.add_parser("work-once")
    listing = commands.add_parser("list")
    listing.add_argument("--limit", type=int, default=100)
    for name in ("get", "cancel"):
        command = commands.add_parser(name)
        command.add_argument("id", type=int)
    schedule = subcommands.add_parser("schedules", help="manage deterministic periodic checks")
    commands = schedule.add_subparsers(dest="schedule_command", required=True)
    add = commands.add_parser("add")
    add.add_argument("name")
    add.add_argument("action")
    add.add_argument("--interval", required=True, type=int)
    add.add_argument("--next-run", type=float, default=0)
    add.add_argument("--payload", default="{}")
    commands.add_parser("list")
    tick = commands.add_parser("tick")
    tick.add_argument("--limit", type=int, default=100)
    for name in ("enable", "disable"):
        command = commands.add_parser(name)
        command.add_argument("id", type=int)


def run(args, operations):
    service = JobService(operations)
    if args.command == "jobs":
        command = args.job_command
        if command == "enqueue":
            return {"job_id": service.enqueue(JobRequest(args.action, args.payload, args.due_at,
                    args.max_attempts, args.retry_delay, args.dedup_key))}
        if command == "work-once":
            return service.work_once()
        if command == "list":
            return service.list(args.limit)
        if command == "get":
            return service.get(args.id)
        return {"cancelled": service.cancel(args.id)}
    command = args.schedule_command
    if command == "add":
        return {"schedule_id": service.add_schedule(Schedule(args.name, args.action, args.interval, args.next_run, args.payload))}
    if command == "list":
        return service.schedules()
    if command == "tick":
        return {"jobs": service.tick(args.limit)}
    service.enable_schedule(args.id, command == "enable")
    return {"enabled": command == "enable"}
