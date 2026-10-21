"""Inspect layered configuration without starting services or mutating data."""
from .application.configuration import ConfigurationService
from .cli_workflows import read_json

def configure(commands):
    parser=commands.add_parser('configuration',help='inspect layered configuration or compare two files')
    actions=parser.add_subparsers(dest='configuration_command',required=True)
    inspect=actions.add_parser('inspect'); inspect.add_argument('files',nargs='*')
    compare=actions.add_parser('compare'); compare.add_argument('before'); compare.add_argument('after')

def run(args,operations):
    service=ConfigurationService()
    if args.configuration_command=='inspect': return service.inspect(args.files)
    return service.compare(read_json(args.before),read_json(args.after))
