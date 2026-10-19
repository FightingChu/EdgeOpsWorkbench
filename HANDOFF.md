# New Task Handoff

## Current state

The repository has completed the 300-file milestone. It contains the original Stage A vertical slice plus event ingestion/querying, durable jobs and schedules, backups and diagnostics, plugins, resumable workflows, PWA/client contracts, the EOW1 device protocol, bounded media evidence, security audits, and 18 disposable benchmark cases.

Start with:

```powershell
python -m unittest discover -s tests -v
python scripts/verify.py
node --check edgeops/static/app.js
```

## Operator commands

- `python -m edgeops init --data-dir <dir>` initializes schema v4.
- `python -m edgeops demo --data-dir <dir>` loads deterministic devices and readings.
- `python -m edgeops import-events <file> --format jsonl --data-dir <dir>` imports events atomically.
- `python -m edgeops events --limit 50 --data-dir <dir>` queries stable cursor pages.
- `python -m edgeops jobs ...` and `python -m edgeops schedules ...` manage leased work.
- `python -m edgeops workflows ...` validates and resumes versioned workflows.
- `python -m edgeops backup <new-dir> --data-dir <dir>` creates a verified snapshot.
- `python -m edgeops cases list` lists benchmark bundles; `cases setup` copies a disposable target.

## Verified baseline

Verified on 2026-10-19 with Python 3.10:

- 72 repository tests pass.
- `scripts/verify.py` passes in an isolated temporary directory.
- JavaScript syntax checks pass for the dashboard and service worker.
- 310 maintained files are present; generated databases, logs, caches, and bytecode remain ignored.
- All 18 case bundles pass manifest validation, exact fault precondition checks, and setup/reset smoke checks.
- Runtime dependencies remain empty and the default bind remains `127.0.0.1`.

## Design constraints

- Python runtime code stays standard-library only.
- Released SQLite migrations are immutable; schema v4 is the current supported version.
- Imports validate the complete source before opening a write transaction.
- Pagination is bounded and snapshot-based; duplicate event content keeps provenance rows.
- Job and workflow completion checks lease tokens before committing results.
- Benchmark setup writes only to a validated disposable target outside the repository.

## Future work

The next useful expansion is deeper Stage E/F work: a real Tkinter operator shell, a small C protocol agent, simulated firmware deployment states, richer media adapters, and release archive verification. Preserve the current migration and event identity contracts while extending those surfaces.

