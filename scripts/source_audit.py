"""Audit executable source independently from tracked-file and documentation counts."""
import argparse
import ast
from collections import Counter
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]

def tracked_paths(root=ROOT,include_untracked=False):
    args=['git','-C',str(root),'ls-files','--cached','-z']
    if include_untracked: args.extend(['--others','--exclude-standard'])
    output=subprocess.check_output(args).decode('utf-8')
    return sorted(set(output.split(chr(0)))-{''})

def has_implementation(source):
    tree=ast.parse(source)
    excluded=(ast.Import,ast.ImportFrom,ast.Pass,ast.Global,ast.Nonlocal)
    def meaningful(node):
        if isinstance(node,excluded): return False
        if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant): return False
        if isinstance(node,ast.Raise): return False
        if isinstance(node,ast.Return) and isinstance(node.value,(ast.Constant,type(None))): return False
        return True
    return any(isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and any(meaningful(statement) for statement in node.body) for node in ast.walk(tree))

def audit(root=ROOT,include_untracked=False):
    root=Path(root); valid=[]; invalid=[]; excluded=[]
    for relative in tracked_paths(root,include_untracked):
        if not relative.endswith('.py'): continue
        path=root/relative
        try:
            source=path.read_text(encoding='utf-8-sig')
            if has_implementation(source): valid.append(relative)
            else: excluded.append(relative)
        except (OSError,UnicodeError,SyntaxError) as exc: invalid.append({'path':relative,'error':str(exc)})
    counts=Counter(path.split('/')[0] for path in valid)
    operational=[path for path in valid if path.startswith(('edgeops/','plugins/','scripts/','tests/'))]
    return {'valid_python_files':len(valid),'valid_python_without_cases':len(operational),'by_area':dict(sorted(counts.items())),
            'syntax_errors':invalid,'excluded_python':excluded,'valid_paths':valid,
            'method':'AST function or method with executable implementation; excludes import-only, empty, docstring-only, constant-return and raise-only files. No non-Python files counted.'}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--include-untracked',action='store_true')
    parser.add_argument('--minimum',type=int,default=300)
    parser.add_argument('--details',action='store_true')
    args=parser.parse_args(argv)
    result=audit(include_untracked=args.include_untracked)
    if not args.details: result.pop('valid_paths');result.pop('excluded_python')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if not result['syntax_errors'] and result['valid_python_without_cases']>=args.minimum else 1

if __name__=='__main__': raise SystemExit(main())
