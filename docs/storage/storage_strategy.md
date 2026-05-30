# Storage Strategy

Operational Registry owns canonical operational state.

Storage is internal to Operational Registry.

Other modules must not directly read or write Operational Registry tables.

Future modules should interact through approved API/Gateway/contracts after Blueprint approval.

## Current v0.5 strategy

```text
memory = fast development and unit testing
sqlite = local/test persistent storage foundation
postgresql = future strategic production target
Boundary

Repository interfaces are the boundary between domain services and storage.

Services and facade must not depend directly on SQLite or future PostgreSQL.

Production DB strategy and migrations are not approved in v0.5.