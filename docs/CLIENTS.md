# Client profiles

The browser client displays telemetry, devices, incidents, and paginated events. The client modules define local and target environment profiles, snapshot cache state, and summary view models. Their state contract uses a snapshot id to reject older event pages and marks offline or pending-write state as stale.
