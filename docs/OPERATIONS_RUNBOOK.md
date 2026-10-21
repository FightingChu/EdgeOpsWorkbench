# Operations runbook

Use `python -m edgeops --data-dir <dir> init` to initialize the data directory. Device readings and imported events are queried through the CLI and dashboard. Use diagnostics to inspect database integrity, verify backups before restoring to a new directory, and keep the service bound to `127.0.0.1`.
