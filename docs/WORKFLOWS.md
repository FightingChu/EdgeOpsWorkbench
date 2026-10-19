# Workflows

Workflow definitions are versioned JSON. Steps may reference input or earlier successful steps. Dry-run validates the graph without a database row. Resume persists each step result and holds a lease around one step.
