# Operations Handoff

## Project overview

EdgeOps Workbench is a local-first device telemetry, monitoring, and incident-response platform. Its modules cover event ingestion and querying, durable jobs and schedules, backups and diagnostics, plugins, resumable workflows, browser assets and client state, the EOW1 device protocol, media evidence, security audits, and disposable benchmark cases.

## Operator commands

Global options such as `--data-dir` precede the subcommand.

```powershell
python -m edgeops --data-dir <dir> init
python -m edgeops --data-dir <dir> import-events <file> --format jsonl
python -m edgeops --data-dir <dir> events --limit 50
python -m edgeops --data-dir <dir> diagnostics
python -m edgeops --data-dir <dir> backup <new-dir>
python -m edgeops --data-dir <dir> serve --open
python -m edgeops cases list
```

The `jobs`, `schedules`, and `workflows` command groups manage durable execution. The `analytics`, `evaluate-rules`, `configuration`, `convert-events`, `export-events`, and `deployments` commands expose telemetry reports, rule evaluation, configuration inspection, format conversion, snapshot exports, and firmware rollout operations. Backup restoration requires a new destination directory.

## Operational constraints

- Python runtime code uses the standard library only.
- The service binds to `127.0.0.1` by default.
- Schema v5 is supported; released migrations are immutable. Schema v5 adds firmware artifacts, deployment state, and transition evidence.
- Event imports validate the source before committing records and import evidence.
- Event pagination uses bounded snapshot cursors; duplicate content retains provenance.
- Job and workflow completion checks lease tokens before committing results.
- Benchmark setup writes to a disposable target outside the repository.
- Generated databases, logs, caches, and bytecode stay out of Git.

## Maintenance checks

```powershell
python -m unittest discover -s tests -v
python scripts/verify.py
node --check edgeops/static/app.js
python scripts/source_audit.py --minimum 300
```

The AST audit counts 319 executable Python files, including 301 outside `cases/`. That outside-case total contains 172 product/plugin/tool files and 129 test files. Empty, import-only, docstring-only, constant-return, and raise-only files are excluded. The full repository test suite contains 272 tests.

