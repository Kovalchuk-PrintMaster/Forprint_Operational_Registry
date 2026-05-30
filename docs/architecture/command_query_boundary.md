# Command / Query Boundary

Operational Registry v0.2 exposes internal command/query services.

This is not a production API.

Current v0.2 has no FastAPI endpoints, no HTTP routing and no real integration with CRM,
Gateway, Telegram Bot, Website, Accounting Registry, Calculator or Prepress Hub.

## Commands

Commands describe internal operational actions:

```text
CreateClientCommand
CreateOrderCommand
ChangeOrderStatusCommand
CreateOperationalTaskCommand
AssignOperationalTaskCommand
ChangeTaskStatusCommand
AddOperationalNoteCommand
AppendOperationalEventCommand

Commands are transport-agnostic and must not depend on Telegram, CRM, Gateway or HTTP.

Queries

Queries describe operational reads:

GetOrderByIdQuery
ListOrdersByClientQuery
ListTasksByOrderQuery
GetOrderStateQuery
GetOrderHistoryQuery
ListOrdersByStatusQuery

Queries return operational state snapshots, not CRM dashboards and not accounting reports.