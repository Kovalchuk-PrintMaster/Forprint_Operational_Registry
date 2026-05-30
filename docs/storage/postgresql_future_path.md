# PostgreSQL Future Path

ForPrint Core Data strategic target is future local server-side PostgreSQL.

v0.5 does not implement PostgreSQL.

v0.5 does not add production DB deployment.

v0.5 does not add Alembic or production migrations.

The current goal is to keep storage models PostgreSQL-compatible in spirit:

```text
explicit primary keys
JSON reference fields
append-only operational events
repository boundary
no cross-module table access

Future PostgreSQL implementation requires separate Blueprint approval.