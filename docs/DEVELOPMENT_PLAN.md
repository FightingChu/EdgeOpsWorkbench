# EdgeOps Workbench Development Plan

## Objective

Build a coherent local-first operations platform that can support a wide range of engineering benchmark tasks. The product manages simulated edge devices, telemetry, logs, alerts, incidents, configuration changes, media evidence, automation, diagnostics, and authorized security checks.

The repository targets approximately 500 maintained files. File count is a scope budget, not a substitute for behavior. Generated data, caches, build products, copied fixtures, and empty padding files do not count.

## Product principles

1. A useful vertical slice must remain runnable throughout development.
2. Python runtime code remains standard-library only until explicitly changed.
3. Device, data, and incident semantics are documented and tested.
4. Destructive operations require an explicit target and recoverable workflow.
5. Every mutation produces audit evidence.
6. Benchmark scenarios alter disposable copies, not the clean product baseline.
7. Local and target-environment differences are simulated deliberately and reproducibly.

## Stage A: runnable foundation

Status: complete.

Deliverables:

- Package, CLI, configuration, and local HTTP server.
- SQLite schema v1 and repository layer.
- Device registration and deterministic telemetry simulation.
- Threshold rules and incident aggregation.
- Minimal dashboard.
- Unit, workflow, and HTTP smoke tests.
- Verification script and handoff documentation.

Exit gate:

- `python -m unittest discover -s tests -v` passes.
- `python scripts/verify.py` passes from a clean temporary data directory.
- No runtime dependency is declared.

## Stage B: ingestion and query reliability

Target repository size: 110-150 files.

- Add JSONL and plain-text event ingestion.
- Track source file, physical line, byte offset, encoding, and ingest version.
- Add bounded payload and record limits.
- Add stable event fingerprints and idempotent re-import.
- Support pagination, search, severity, service, device, and time filters.
- Introduce schema v2 with migration and downgrade-rejection tests.
- Add malformed, truncated, non-ASCII, duplicate, and oversized fixtures.
- Extend the dashboard with an event table and incident detail view.

Exit gate:

- Re-import does not duplicate events.
- Invalid files do not create partial committed imports.
- Pagination returns stable, non-overlapping pages.
- Full dataset tests include counterexamples absent from the sample fixture.

## Stage C: monitoring, jobs, and diagnostics

Target repository size: 190-240 files.

- Add scheduled checks with injectable clocks.
- Add retry, backoff, cancellation, and dead-letter state.
- Add service health snapshots and incident timelines.
- Add backup, restore-to-new-directory, and read-only diagnostics.
- Add configuration validation and layered defaults.
- Add CLI subcommands for jobs, incidents, diagnostics, and backup.
- Add concurrency and restart recovery tests without long sleeps.

Exit gate:

- Restart preserves pending work exactly once.
- Backup verification detects truncation and schema mismatch.
- Failed migrations and job mutations roll back atomically.

## Stage D: plugin and workflow platform

Target repository size: 270-320 files.

- Define versioned plugin manifests and capability boundaries.
- Add rule, importer, exporter, and diagnostic plugin interfaces.
- Add declarative workflow definitions and validation.
- Add dry-run, execution logs, cancellation, and resumable steps.
- Add sample plugins without external packages.
- Add compatibility fixtures for old plugin and workflow versions.

Exit gate:

- Unsupported versions fail with actionable errors.
- Plugin failures cannot corrupt the main transaction.
- Paired encode/decode and import/export behavior remains symmetric.

## Stage E: clients and target environments

Target repository size: 340-390 files.

- Expand the web client into an installable PWA.
- Add offline read cache and explicit stale-state indicators.
- Add a Tkinter desktop operator client.
- Add local and target environment profiles with real path, encoding, timezone, and Python-version differences.
- Add browser and desktop lifecycle/concurrency regression cases.

Exit gate:

- Target-profile tests exercise behavior not covered by syntax checks.
- Clients reject stale writes and recover after reconnect.
- Accessibility and narrow-screen smoke checks pass.

## Stage F: device protocol, firmware, and media

Target repository size: 410-455 files.

- Specify a framed binary device protocol with checksums and version negotiation.
- Add a deterministic Python device simulator.
- Add a small C agent and host-side build/test harness.
- Add configuration and simulated firmware deployment state machines.
- Add image evidence ingestion, thumbnail metadata, and bounded media processing.
- Add device and media corruption fixtures.

Exit gate:

- Protocol parser round trips and rejects malformed lengths/checksums.
- Failed deployments recover without claiming success.
- Existing callers remain compatible after protocol changes.

## Stage G: security, benchmark cases, and release

Target repository size: 480-520 files.

- Add authorized local configuration and endpoint audit checks.
- Add artifact hashing, evidence manifests, and redacted diagnostic exports.
- Implement the case manifest schema and disposable setup runner.
- Build public checks and private-verifier contracts for each mechanism family.
- Add CI, reproducible release archives, upgrade matrices, and release verification.
- Complete operator, developer, protocol, plugin, and case-author documentation.

Exit gate:

- Clean main passes all tests on supported Python versions.
- Every benchmark case has deterministic setup, verification, and reset behavior.
- Scenario metadata records domain, subdomain, mechanism, category, rounds, constraints, and expected evidence.
- Release archives exclude databases, logs, secrets, and private verifier material.

## Benchmark coverage strategy

Prioritize the mechanism families that dominate the source workbook:

1. Goal understanding and persistent constraints.
2. Verification depth and target-environment checks.
3. Root-cause diagnosis and failure recovery.
4. Implementation boundaries and regression control.
5. Planning efficiency and completion claims.
6. Tool preconditions, collaboration behavior, and authorization boundaries.

Representative cases include sample-versus-full-data contradictions, misleading surface errors, ready-made validation commands, unavailable verification tools, stale runtime copies, paired branches, non-ASCII input, concurrent writes, interrupted migrations, prohibited new dependencies, and tempting destructive targets.

## Delivery cadence

- Keep commits vertical and reviewable.
- Finish one stage gate before broadening the next module.
- Update `HANDOFF.md` after each stage.
- Update `docs/FILE_BUDGET.md` with actual maintained-file counts.
- Do not create placeholder modules solely to approach 500 files.


