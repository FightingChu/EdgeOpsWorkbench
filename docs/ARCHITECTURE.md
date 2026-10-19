# Architecture

## System context

EdgeOps Workbench runs on one operator machine. Simulated or authorized test devices send readings to a local service. The service validates input, persists evidence, evaluates deterministic rules, and exposes query results to CLI, browser, and future desktop clients.

```text
Device simulator / C agent
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
          Web/PWA     CLI/Desktop
```

## Dependency direction

Dependencies point inward:

- Domain imports only standard-library value types.
- Application imports domain contracts and persistence interfaces.
- Persistence implements storage and transaction boundaries.
- API and CLI translate external input into application calls.
- Device adapters translate protocol data into domain input.

The domain layer must never import SQLite, HTTP handlers, filesystem paths, browser state, or client code.

## Initial data model

- `devices`: registered logical devices and last-seen state.
- `telemetry`: immutable metric readings.
- `incidents`: current aggregated threshold violations.
- `meta`: schema version and future database metadata.

Telemetry identity is assigned at ingestion. Future event ingestion adds source fingerprints so repeated imports can be idempotent.

## Transaction rules

- Registering a device and ingesting one reading are separate explicit actions.
- A reading and the incident change it triggers commit in one transaction.
- Validation occurs before mutation.
- Database migrations run transactionally and reject unsupported newer schemas.
- Future destructive maintenance operations must create or verify a recoverable backup first.

## HTTP boundary

The server binds to `127.0.0.1` by default and emits no-cache and defensive browser headers. The initial API is read-only; later mutations require a per-process session token and origin checks.

## Benchmark isolation

The clean repository is never intentionally broken. A case setup script copies or patches a disposable workspace, records the starting hash, and exposes only the public task material. Verification checks behavior and required evidence; reset deletes only the validated disposable target.

