# Non-goals and Boundaries

## Purpose

This document defines what Local Launch Readiness v0.1 does not implement.

Operational Registry remains the operational truth layer and internal data custodian.

This checkpoint is local/offline only.

## Live integration boundary

This checkpoint explicitly preserves the live integration boundary.

Operational Registry must not connect to live CRM, Telegram, Website, 1C, Accounting Registry, Calculator, Library, Warehouse or Prepress runtime systems in this phase.

## Non-goals

Local Launch Readiness v0.1 does not implement:

```text
production API;
live CRM integration;
live Telegram integration;
live Website integration;
real 1C sync/write;
automatic posting;
Accounting payment truth;
Library catalog ownership;
Warehouse stock truth;
Calculator final pricing ownership;
Prepress lifecycle ownership;
production task dispatch;
customer-facing runtime UI.
Accounting boundary

Operational Registry may store accounting references and payment projection references.

It must not become the accounting truth owner.

It must not post accounting documents.

It must not write to 1C.

Library boundary

Operational Registry may store canonical reference IDs supplied by Library.

It must not own canonical product, service, material, operation or alias semantics.

Ambiguous or missing canonical semantics must be routed to Library governance later.

Calculator boundary

Operational Registry may store Calculator output package references and local order draft references.

It must not calculate final prices.

It must not own pricing formulas.

It must not replace Calculator Engine.

Warehouse boundary

Operational Registry may store material requirement references or operational projections.

It must not become warehouse stock truth.

It must not reserve stock in a live warehouse system.

CRM/channel boundary

Operational Registry may support future CRM or channel adapters through references and contracts.

It must not become a CRM dashboard.

It must not become Telegram, Website or Mobile App runtime.

Prepress boundary

Operational Registry may store prepress-related references in future boundary-safe contracts.

It must not own the Prepress lifecycle.

It must not process production files.

Allowed local scope

Allowed work in this checkpoint:

local/offline docs;
safe local examples;
local check-report improvements;
local command/query readiness checks;
local completion coordination automation;
coordination status/report updates.

---