# EdgeOps Workbench

EdgeOps Workbench is a local-first device telemetry and incident-response platform. It accepts deterministic simulated device readings, stores them in SQLite, applies threshold rules, opens or updates incidents, and exposes the current state through a CLI and a browser dashboard.

The current implementation also includes durable jobs and workflows, subprocess plugins, a PWA shell, client state contracts, a framed device protocol, bounded media evidence, security audits, and isolated benchmark scenarios. Runtime code uses only Python 3.10+ standard-library modules.

## Quick start

```powershell
python -m edgeops init
python -m edgeops demo
python -m edgeops summary
python -m edgeops serve --open
```

The default dashboard is `http://127.0.0.1:8877`. Runtime data is stored under `data/` and is ignored by Git.

## Current vertical slice

- Versioned SQLite initialization through schema v4.
- Device registration, deterministic telemetry, threshold rules, and incident aggregation.
- JSONL/text event ingestion with stable fingerprints, provenance, filters, and keyset pagination.
- Lease-based jobs, retries, cancellation, schedules, backups, diagnostics, plugins, and workflows.
- EOW1 framed protocol, media evidence manifests, client profiles, and 18 disposable benchmark cases.
- Local dashboard and CLI with 72 unit, workflow, reliability, and boundary tests.

Run the current verification suite:

```powershell
python -m unittest discover -s tests -v
python scripts/verify.py
```

See `docs/DEVELOPMENT_PLAN.md`, `docs/ARCHITECTURE.md`, `docs/FILE_BUDGET.md`, and `HANDOFF.md` for implementation details and continuation points.

