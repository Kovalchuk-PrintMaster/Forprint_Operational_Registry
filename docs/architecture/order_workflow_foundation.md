# Order Workflow Foundation

Operational Registry owns flexible operational order/workflow/projection records.

This foundation is not a final production order system.

## Owns

```text
OperationalOrder
OperationalOrderLine
WorkflowStage
MaterialRequirement
PaymentProjection
AlertRule
AlertEvent
Operational report projections
Terminal previews
Does not own
Calculator formulas or pricing rules
Library canonical product/material/service semantics
Accounting posting or 1C synchronization
Warehouse stock truth
Telegram runtime UI
CRM dashboard UI
Prepress file lifecycle truth

Use references instead of foreign-domain ownership.