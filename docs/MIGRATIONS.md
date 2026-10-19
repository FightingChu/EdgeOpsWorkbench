# Migration policy

Released schema files are immutable. New tables arrive in the next migration module. Initialization executes each DDL statement under the database transaction so injected migration failures leave no partial tables or version update.
