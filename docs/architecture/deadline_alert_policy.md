# Deadline and Alert Policy

Operational Registry may create deadline control records and alert events.

Allowed alert behavior:

```text
late workflow stage -> alert event
overdue payment projection -> alert event
unresolved material requirement -> alert event
manual review stale -> alert event

No real Telegram sending.

No CRM popup.

No web UI.

AlertEvent is a record only.