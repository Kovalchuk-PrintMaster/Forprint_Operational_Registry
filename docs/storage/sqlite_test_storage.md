# SQLite Test Storage

SQLite is approved in v0.5 for local/test persistent storage.

SQLite storage may persist:

```text
client_record
order
operational_task
operational_event
operational_note
operational_blocker

SQLite storage must not become production deployment strategy.

SQLite storage must remain behind repository interfaces.

No external modules may directly access SQLite tables.