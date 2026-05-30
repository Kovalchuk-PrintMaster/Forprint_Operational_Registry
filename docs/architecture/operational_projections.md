# Operational Projections

Operational Registry v0.3 provides internal read-side operational projections.

These projections may answer:

```text
current order state
current task state
active blockers
operational readiness
payment reference status
prepress reference status
calculator quote reference status
timeline of operational events
orders needing manual review
orders blocked by missing inputs

They must not answer:

real payment balance
invoice truth
CRM dashboard layout
product/material catalog truth
warehouse stock quantity
real prepress output files

Operational projections are internal readiness models for future CRM, Telegram status display,
Gateway routing feedback and Project Inspector summaries.

No production API is introduced in v0.3.