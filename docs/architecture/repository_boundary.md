```md
# Repository Boundary

Operational Registry v0.2 defines repository interfaces before production storage.

Repository interfaces are storage-agnostic.

Allowed v0.2 implementation:

```text
InMemoryClientRepository
InMemoryOrderRepository
InMemoryTaskRepository
InMemoryOperationalEventRepository
InMemoryOperationalNoteRepository

Not approved in v0.2:

PostgreSQL production storage
database migrations
full event store
multi-tenant storage

The goal is to stabilize service contracts before locking storage design.