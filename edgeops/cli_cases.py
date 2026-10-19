"""Discover, create, verify, and explicitly reset disposable benchmark copies."""

from .benchmark import list_cases, reset_case, setup_case
from .benchmark.catalog import ROOT
from .benchmark.verifier import verify_case


def configure(subcommands):
    cases = subcommands.add_parser("cases", help="manage isolated benchmark copies")
    commands = cases.add_subparsers(dest="case_command", required=True)
    commands.add_parser("list")
    for name in ("setup", "verify"):
        command = commands.add_parser(name)
        command.add_argument("id")
        command.add_argument("--target", required=True)
    reset = commands.add_parser("reset")
    reset.add_argument("--target", required=True)


def run(args):
    if args.case_command == "list":
        return list_cases()
    if args.case_command == "reset":
        reset_case(args.target)
        return {"reset": True}
    manifests = {case["id"]: case for case in list_cases()}
    if args.id not in manifests:
        raise ValueError("unknown case id")
    case = ROOT / "cases" / args.id
    if args.case_command == "setup":
        marker = setup_case(case, args.target)
        return {"case_id": marker["case_id"], "target": marker["target"]}
    return verify_case(case, args.target)
