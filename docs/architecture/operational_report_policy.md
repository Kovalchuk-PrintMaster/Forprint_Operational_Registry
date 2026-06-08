# Operational Report Policy

Operational Registry may produce demo/read-side operational projections.

Required future report types:

```text
client_order_history
client_product_service_history
material_requirements_by_period
payment_debt_summary
workflow_stage_status
late_orders
late_workflow_stages
contractor_workload
contractor_blockers
deadline_risk
alert_summary

Reports should be built from dimensions, facts, events, projections and references.

Reports must not become accounting truth, warehouse truth or CRM dashboard layout.


---