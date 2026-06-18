# Local Operator Workflow

## Purpose

This document describes the offline local workflow for using Operational Registry as an internal operational registry foundation.

No production API, UI or live integration is required for this workflow.

## Workflow overview

```text
order context
↓
workflow/projection
↓
blockers/readiness
↓
previews/reports
↓
completion/status export
Step 1 — Order context

The operator starts from a safe local order context.

The order context may include:

client/account reference;
order reference;
order lines;
workflow stage references;
payment projection references;
material requirement references;
deadline and blocker information.

The context must use safe example data only.

No real customer production data is required for this local workflow.

Step 2 — Workflow/projection

The operator can inspect local workflow and projection examples through:

make order-preview
make workflow-preview
make operational-report-preview

These commands are terminal previews only.

They do not create production tasks, send messages or mutate external systems.

Step 3 — Blockers/readiness

The operator can inspect readiness and blocker-related examples through the existing local reports and previews.

The goal is to verify that Operational Registry can represent:

workflow stages;
deadline controls;
operational blockers;
payment projection references;
material requirement references;
alert events;
readiness signals.

These are local/offline representations, not live process automation.

Step 4 — Previews/reports

The operator validates the local state using:

make check-report
make check

The check-report confirms that local models, fixtures, previews, documentation, coordination metadata and boundary rules are valid.

Step 5 — Completion/status export

The operator can export current module status using:

make status-report

The status export is a local coordination artifact.

It does not publish a production runtime state and does not synchronize to external systems.

Operational safety

The local operator workflow must remain boundary-safe.

It must not:

send Telegram messages;
create CRM dashboard records;
write to 1C;
post accounting documents;
reserve warehouse stock;
call Calculator for final prices;
edit Library catalog semantics;
control Prepress lifecycle.
Expected local result

After the workflow, the operator should know:

whether the repository is clean;
whether Blueprint instruction intake is visible;
whether Blueprint standards are visible;
whether tests/check-report/governance-check are green;
whether local previews render correctly;
whether coordination records are current.

---