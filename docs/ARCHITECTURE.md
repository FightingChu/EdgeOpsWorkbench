# Architecture

## System context

EdgeOps Workbench runs on one operator machine. Device adapters and deterministic simulators supply readings to application services. The services validate input, persist evidence, evaluate rules, and expose query results through the CLI and local HTTP API.

```text
Device adapters / simulator
            |
            v
      Application services
       /       |        \
   Domain   Persistence   Audit
      |          |          |
      +------- SQLite ------+
                 |
           Local HTTP API
             /        \
       Browser client    CLI
```

## Dependency direction

Dependencies point inward:

- Domain imports only standard-library value types.
- Application imports domain contracts and persistence interfaces.
- Persistence implements storage and transaction boundaries.
- API and CLI translate external input into application calls.
- Device adapters translate protocol data into domain input.

The domain layer must never import SQLite, HTTP handlers, filesystem paths, browser state, or client code.

## Data model

- `devices`: registered logical devices and last-seen state.
- `telemetry`: immutable metric readings.
- `incidents`: current aggregated threshold violations.
- `meta`: schema version and database metadata.
- `events`: normalized immutable event content and unique fingerprints.
- `event_imports` and `event_origins`: import audit records and physical source coordinates.
- `jobs` and `job_runs`: durable requests, leases, results, and execution attempts.
- `schedules` and `health_snapshots`: periodic dispatch state and recorded check results.
- `workflow_runs` and `workflow_steps`: persisted workflow definitions, progress, and step results.
- `audit_entries`: transaction-local mutation evidence.
- `firmware_artifacts`: immutable firmware release descriptors with digest and size.
- `deployments` and `deployment_transitions`: revision-checked deployment state and ordered transition evidence.

Telemetry identity is assigned at ingestion. Event fingerprints identify normalized content; repeated imports retain their source origins without duplicating event content.

## Transaction rules

- Registering a device and ingesting one reading are separate explicit actions.
- A reading and the incident change it triggers commit in one transaction.
- Validation occurs before mutation.
- Database migrations run transactionally and reject unsupported newer schemas.
- Backup verification checks hashes and database integrity. Restoration writes to a new directory.
- Job and workflow results commit only while their lease tokens are current.
- Firmware deployment transitions and audit evidence commit together. Concurrent writers must supply the current revision; transfer completion requires the descriptor's exact byte count.

## HTTP boundary

The server binds to `127.0.0.1` by default and emits no-cache and defensive browser headers. The HTTP API is read-only and exposes health, summary, devices, incidents, telemetry, event queries, and event filter values. CLI commands translate imports and other mutations into application service calls.

## Benchmark isolation

The clean repository is never intentionally broken. A case setup script copies or patches a disposable workspace, records the starting hash, and exposes only the public task material. Verification checks behavior and required evidence; reset deletes only the validated disposable target.
