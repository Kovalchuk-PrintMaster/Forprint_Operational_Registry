# Command Envelope

Operational Registry v0.3 introduces a local future-facing command envelope.

The envelope is internal and offline.

It is not:

```text
Gateway
transport router
production API
HTTP contract
message queue
event bus
Purpose

The local envelope helps Operational Registry understand the shape of future operational commands.

Future sources may include:

CRM
Integration Gateway
Telegram Bot through Gateway/CRM flow
Website through Gateway/CRM flow
future Mobile App through Gateway/CRM flow
Boundary

Operational Registry may normalize command shape for its own internal services.

Operational Registry must not route commands.

Future runtime transport belongs to Integration Gateway.

Future canonical contract truth belongs to ForPrint Library.