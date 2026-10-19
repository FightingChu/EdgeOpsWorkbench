# EdgeOps Workbench Agent Instructions

## Project intent

EdgeOps Workbench is a local-first device telemetry, monitoring, incident-response, and task-case platform. The repository is deliberately broad enough to support backend, frontend, data, operations, CLI, client, embedded, media, and security engineering tasks without becoming a collection of unrelated demos.

## Hard constraints

- Keep the Python runtime dependency-free. `pyproject.toml` must retain `dependencies = []` unless the operator explicitly changes this rule.
- Bind services to `127.0.0.1` by default. Do not expose the server publicly without explicit authorization.
- Preserve SQLite migration compatibility. Never edit an existing migration after release; add the next migration.
- Never silently drop or duplicate telemetry events.
- Main must remain healthy. Benchmark defects belong in isolated copies created by `cases/<id>/setup.py`.
- Tests must not require the public internet or long wall-clock sleeps.
- Keep generated databases, logs, build outputs, and scenario worktrees out of Git.
- Do not manufacture files to hit the 500-file budget. Every maintained file needs a clear owner and purpose.

## Architecture boundaries

- `edgeops/domain`: deterministic business rules and typed values. No SQLite, HTTP, filesystem, or browser concerns.
- `edgeops/application`: use cases and transaction orchestration.
- `edgeops/persistence`: SQLite schema, migrations, repositories, backup, and diagnostics.
- `edgeops/api`: local HTTP boundary and static assets.
- `edgeops/devices`: protocol adapters and deterministic simulators.
- `cases`: task metadata, setup scripts, public checks, and private-verifier contracts.
- `tests`: unit, integration, HTTP, migration, concurrency, and regression tests.

## Required checks

Run before handing off code changes:

```powershell
python -m unittest discover -s tests -v
python scripts/verify.py
```

For JavaScript changes, also run `node --check edgeops/static/app.js` when Node.js is available.

## Current stage

Stage A bootstrap is implemented. Read `HANDOFF.md`, `docs/DEVELOPMENT_PLAN.md`, and `docs/ARCHITECTURE.md` before expanding the project.

