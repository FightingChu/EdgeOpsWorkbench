# Event ingestion

JSONL imports are parsed completely before a transaction begins. Each accepted record has a stable content fingerprint and a physical source coordinate. Duplicate content keeps an origin row and increments the import duplicate count. A malformed tail rolls back the audit row and all event rows.
