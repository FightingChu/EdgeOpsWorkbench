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

## Features

- Versioned SQLite initialization through schema v5.
- Device registration, deterministic telemetry, threshold rules, and incident aggregation.
- JSONL/text event ingestion with stable fingerprints, provenance, filters, and keyset pagination.
- Lease-based jobs, retries, cancellation, schedules, backups, diagnostics, plugins, and workflows.
- EOW1 framed protocol, media evidence manifests, client profiles, and 18 disposable benchmark cases.
- Per-device telemetry statistics, quantiles, trend fitting, and anomaly analysis.
- Composable event rules, grouped alert identities, notification policy, and lifecycle transitions.
- Layered configuration, strict INI/JSON adapters, redaction, and atomic object patching.
- JSON, NDJSON, CSV, XML, syslog, and CloudEvents decoding; snapshot exports and bounded binary codecs.
- Firmware descriptors, chunk verification, canary plans, checkpoints, rollback policy, and durable simulated deployments.
- Local dashboard and CLI with 272 unit, workflow, reliability, and boundary tests.

## Source audit

`python scripts/source_audit.py --minimum 300` checks tracked Python source with executable function or method bodies. It excludes empty files, pure imports, docstring-only modules, constant-return functions, and raise-only functions. The repository has 319 qualifying Python files: 301 outside `cases/` (172 product/plugin/tool files and 129 test files), plus 18 case tests. Markdown, JSON fixtures, CSS, and HTML do not contribute to this count.

Run the current verification suite:

```powershell
python -m unittest discover -s tests -v
python scripts/verify.py
python scripts/source_audit.py --minimum 300
```

See `docs/ARCHITECTURE.md` for architecture, `docs/DEVELOPMENT_PLAN.md` for module responsibilities and maintenance rules, `docs/FILE_BUDGET.md` for the file inventory, and `HANDOFF.md` for operational commands.

