"""Telemetry reports expose numeric analysis through the existing CLI."""
from .application.analytics import AnalyticsService

def configure(commands):
    parser=commands.add_parser('analytics',help='summarize persisted telemetry by device and metric')
    parser.add_argument('metric'); parser.add_argument('--device-id'); parser.add_argument('--limit',type=int,default=1000)

def run(args,operations):
    return AnalyticsService(operations).report(args.metric,args.device_id,args.limit)
