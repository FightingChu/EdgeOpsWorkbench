"""Firmware registration, rollout state, and deterministic simulation commands."""
from .application.deployments import DeploymentService
from .domain.deployment.planning import plan
from .domain.deployment.policy import RolloutPolicy
from .cli_workflows import read_json

def configure(commands):
    parser=commands.add_parser('deployments',help='register firmware and manage durable simulated rollouts')
    actions=parser.add_subparsers(dest='deployment_command',required=True)
    register=actions.add_parser('register'); register.add_argument('path'); register.add_argument('--version',required=True)
    create=actions.add_parser('create'); create.add_argument('device_id'); create.add_argument('artifact_id',type=int)
    get=actions.add_parser('get'); get.add_argument('id',type=int)
    advance=actions.add_parser('advance'); advance.add_argument('id',type=int); advance.add_argument('revision',type=int); advance.add_argument('action'); advance.add_argument('--received-bytes',type=int)
    simulation=actions.add_parser('simulate'); simulation.add_argument('id',type=int); simulation.add_argument('path'); simulation.add_argument('--fail-at',choices=('transfer','verify','apply'))
    planning=actions.add_parser('plan'); planning.add_argument('inventory'); planning.add_argument('manifest'); planning.add_argument('--batch-size',type=int,default=10)

def run(args,operations):
    service=DeploymentService(operations); action=args.deployment_command
    if action=='register': return service.register(args.path,args.version)
    if action=='create': return service.create(args.device_id,args.artifact_id)
    if action=='get': return service.get(args.id)
    if action=='advance': return service.advance(args.id,args.revision,args.action,args.received_bytes)
    if action=='plan': return plan(read_json(args.inventory),read_json(args.manifest),RolloutPolicy(batch_size=args.batch_size))
    return service.run_simulation(args.id,args.path,args.fail_at)
