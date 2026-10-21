# EdgeOps Workbench Agent Instructions

## Project intent

EdgeOps Workbench is a local-first device telemetry, monitoring, incident-response, and task-case platform. Its modules cover backend services, browser interfaces, data processing, operations, CLI tools, client state, device protocols, media evidence, and security checks.

## Hard constraints

- Keep the Python runtime dependency-free. `pyproject.toml` must retain `dependencies = []` unless the operator explicitly changes this rule.
- Bind services to `127.0.0.1` by default. Do not expose the server publicly without explicit authorization.
- Preserve SQLite migration compatibility. Never edit an existing migration after release; add the next migration.
- Never silently drop or duplicate telemetry events.
- Main must remain healthy. Benchmark defects belong in isolated copies created by `cases/<id>/setup.py`.
- Tests must not require the public internet or long wall-clock sleeps.
- Keep generated databases, logs, build outputs, and scenario worktrees out of Git.
- Every maintained file needs a clear owner and purpose; do not add empty or duplicate files.

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

## Project documentation

Read `HANDOFF.md` for operations, `docs/DEVELOPMENT_PLAN.md` for module responsibilities and maintenance rules, and `docs/ARCHITECTURE.md` for system boundaries and transaction rules.
