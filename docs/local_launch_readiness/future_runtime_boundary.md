# Future Runtime Boundary

## Purpose

This document describes the future runtime/API/integration boundary as design-only guidance.

It does not implement production runtime code.

It does not authorize production API, live integrations or external writes.

## Current state

Operational Registry currently provides local/offline foundations:

```text
models;
DTOs;
repository interfaces;
SQLite/local storage foundation;
safe fixtures;
terminal previews;
check-report;
coordination reports;
module status export.
Future API boundary

A future API boundary may expose carefully scoped command/query operations.

Possible future command/query categories:

create or update operational order records;
read client/order/workflow projections;
record operational blocker state;
read readiness summaries;
export operational status snapshots;
resolve local references against approved canonical IDs.

This future API must remain behind explicit Blueprint approval.

No production API is added in this checkpoint.

Future integration boundary

Future integrations may connect through dedicated modules or adapters.

Expected ownership remains:

Integration Gateway: runtime validation/routing/idempotency/correlation;
Calculator Engine: calculation and order formalization output;
Library: canonical semantic/catalog authority;
Accounting Registry: accounting/1C synchronization boundary;
Warehouse Service: stock and material operations;
CRM: human dashboard/workflow coordination;
Telegram/Website/Mobile App: customer channels;
Prepress Hub: prepress/file preparation lifecycle.

Operational Registry should receive structured references and store operational truth.

It should not take over foreign module responsibilities.

Future contract principles

Any future runtime contract should follow these rules:

stable IDs over names;
explicit source system references;
idempotent write commands;
audit-friendly state transitions;
clear ownership boundaries;
no hidden cross-module mutation;
safe rollback or replay strategy where needed;
no direct 1C production write from Operational Registry.
Future API readiness gates

Before any production API can be added, Blueprint should explicitly approve:

API boundary document;
command/query contract shape;
authentication/authorization approach;
idempotency policy;
audit/event policy;
integration ownership map;
test coverage;
rollback strategy;
data privacy approach.
Current checkpoint boundary

This document is design-only.

It does not add:

FastAPI;
Django;
Flask;
HTTP routes;
background workers;
message queues;
runtime adapters;
1C writers;
CRM connectors;
Telegram handlers;
Warehouse connectors;
Prepress processors.

---