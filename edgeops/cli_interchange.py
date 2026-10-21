"""CLI conversion and database export use exclusive output files."""
from .application.interchange import InterchangeService
from .application.exports import ExportService
from .codecs.registry import formats

def configure(commands):
    convert=commands.add_parser('convert-events',help='convert event files into JSON, NDJSON or CSV')
    convert.add_argument('source'); convert.add_argument('destination'); convert.add_argument('--from-format',required=True,choices=formats()); convert.add_argument('--to-format',default='ndjson',choices=('json','ndjson','csv')); convert.add_argument('--encoding',default='utf-8')
    export=commands.add_parser('export-events',help='export a bounded event snapshot to a new file')
    export.add_argument('destination'); export.add_argument('--format',default='ndjson',choices=('json','ndjson','csv')); export.add_argument('--limit',type=int,default=10000)

def run(args,operations):
    if args.command=='convert-events': return InterchangeService().convert(args.source,args.destination,args.from_format,args.to_format,args.encoding)
    return ExportService(operations).export(args.destination,args.format,args.limit)
