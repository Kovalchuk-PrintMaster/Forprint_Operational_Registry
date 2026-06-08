# Event Log Policy

Operational events are append-only history records.

Events should help reconstruct history and debug workflow changes.

Do not use only mutable final state.

Examples:

```text
order_created
order_status_changed
payment_seen
workflow_stage_started
workflow_stage_completed
material_required
material_reserved
manual_review_requested

Events do not replace domain ownership rules.