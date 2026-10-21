"""Evaluate explicit JSON alert rules against persisted event pages."""
from .application.alerting import AlertingService
from .cli_workflows import read_json
from .domain.event_query import EventQuery

def configure(commands):
    parser=commands.add_parser('evaluate-rules',help='evaluate a JSON rule set against events')
    parser.add_argument('rules'); parser.add_argument('--limit',type=int,default=50); parser.add_argument('--cursor')

def run(args,operations):
    return AlertingService(operations).evaluate(read_json(args.rules),EventQuery(limit=args.limit,cursor=args.cursor))
