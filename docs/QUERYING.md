# Event querying

Queries are bounded to 200 rows. A cursor contains a fixed insertion snapshot and a filter digest. Keyset pagination orders by immutable event id, so new events do not change earlier pages. Search text is escaped before it reaches SQLite LIKE.
