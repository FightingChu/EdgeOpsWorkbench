# Development and Maintenance

## Product modules

EdgeOps Workbench organizes local device operations around the following modules.

| Module | Responsibilities |
| --- | --- |
| Telemetry and incidents | Device registration, immutable readings, threshold rules, and incident aggregation |
| Event ingestion and queries | JSONL/text import, physical source coordinates, content fingerprints, filters, and snapshot cursors |
| Jobs and schedules | Durable task state, leases, retries, cancellation, periodic dispatch, and health snapshots |
| Backups and diagnostics | SQLite snapshots, manifest checks, restoration to new directories, and read-only diagnostics |
| Plugins and workflows | Versioned manifests, subprocess JSON calls, declarative steps, persisted results, and resume/cancel operations |
| Browser and client modules | Dashboard, event table, incident details, service worker assets, profiles, cache state, and summary view models |
| Devices and evidence | EOW1 frame parsing, CRC32, reading messages, protocol negotiation, evidence hashing, and metadata |
| Security and cases | Local configuration/header checks, redacted reports, case manifests, isolated fault injection, and reset |
| Telemetry analytics | Per-device rollups, quantiles, dispersion, smoothing, regression, anomaly detection, rates, and availability |
| Alert policies | Typed predicates, composite conditions, grouping, cooldowns, hysteresis, silences, routing, and escalation |
| Configuration | Layered values, environment allowlist, strict INI/JSON loading, path bounds, redaction, diffs, and atomic patching |
| Event interchange | Bounded event decoders, CSV/JSON/NDJSON exports, checksummed envelopes, gzip limits, and sequence tracking |
| Firmware deployment | Artifact identity, chunk/checkpoint verification, canary waves, compatibility, persistent transitions, and simulation |

## Dependency boundaries

Domain values and rules are deterministic. Application services coordinate use cases. Persistence owns SQLite transactions and migrations. CLI, HTTP, and device adapters translate external input into service calls. See `docs/ARCHITECTURE.md` for the data model and transaction rules.

## Maintenance rules

1. Keep Python runtime dependencies empty and bind services to loopback by default.
2. Add a migration for schema changes; preserve released migration definitions.
3. Preserve telemetry identity, event fingerprints, source coordinates, and import atomicity.
4. Keep job/workflow lease checks and durable results consistent across retries and restarts.
5. Keep benchmark faults inside disposable copies with explicit target paths.
6. Exclude generated databases, logs, caches, and build outputs from version control.
7. Keep operational documentation aligned with commands and implemented interfaces.

## Developer commands

```powershell
python -m unittest discover -s tests -v
python scripts/verify.py
node --check edgeops/static/app.js
python scripts/source_audit.py --minimum 300
```

Tests use isolated data directories and deterministic inputs. The independent verification script exercises telemetry, event import, durable jobs, workflows, protocol parsing, and the case catalog.


