# Operational Registry Order / Workflow / Projection Foundation v0.1 Report

## 1. Files added/changed

```text
app/forprint_operational_registry/models/order_workflow.py
app/forprint_operational_registry/services/order_workflow_demo.py
scripts/order_workflow_preview.py
examples/order_workflow/*
docs/architecture/order_workflow_foundation.md
docs/architecture/calculator_output_package_reference_policy.md
docs/architecture/product_service_reference_policy.md
docs/architecture/material_requirement_policy.md
docs/architecture/payment_projection_policy.md
docs/architecture/workflow_stage_policy.md
docs/architecture/contractor_subcontractor_tracking_policy.md
docs/architecture/deadline_alert_policy.md
docs/architecture/operational_report_policy.md
tests for order/workflow models, services, previews, docs and examples
check-report validations
Makefile preview targets
coordination status/report updates
2. Models/DTOs added
OperationalOrder
OperationalOrderLine
CalculatorOutputPackageReference
ProductServiceReference
MaterialRequirement
PaymentProjection
WorkflowStageTemplate
WorkflowTemplate
WorkflowStage
ContractorReference
DeadlineControlRecord
AlertRule
AlertEvent
3. Services/helpers added
OrderWorkflowDemoService
WorkflowStageService
MaterialRequirementService
PaymentProjectionService
AlertEvaluationService
OperationalReportService
demo_workflow_template
4. Fixtures added
examples/order_workflow/demo_order.yaml
examples/order_workflow/demo_order_lines.yaml
examples/order_workflow/demo_calculator_reference.yaml
examples/order_workflow/demo_product_service_references.yaml
examples/order_workflow/demo_material_requirements.yaml
examples/order_workflow/demo_payment_projection.yaml
examples/order_workflow/demo_workflow_template.yaml
examples/order_workflow/demo_workflow_stages.yaml
examples/order_workflow/demo_contractor_references.yaml
examples/order_workflow/demo_deadlines.yaml
examples/order_workflow/demo_alerts.yaml
examples/order_workflow/demo_report_projections.yaml
5. Terminal previews added
make order-preview
make workflow-preview
make payment-preview
make material-requirement-preview
make alert-preview
make operational-report-preview
6. Architecture docs added
order_workflow_foundation.md
calculator_output_package_reference_policy.md
product_service_reference_policy.md
material_requirement_policy.md
payment_projection_policy.md
workflow_stage_policy.md
contractor_subcontractor_tracking_policy.md
deadline_alert_policy.md
operational_report_policy.md
7. Calculator reference preparation

Calculator references are stored as IDs/refs only.

Operational Registry does not own formulas, pricing rules or calculation package generation.

8. Product/service reference preparation

Product/service display and raw names are preserved.

Future Library IDs are optional references.

Library remains owner of canonical product/service/material semantics.

9. Material requirement behavior

MaterialRequirement stores planned material needs and unresolved statuses.

Warehouse remains future owner of stock/reservation truth.

10. Payment projection behavior

PaymentProjection stores operational payment/debt visibility.

Accounting Registry remains owner of accounting sync, payment truth and 1C posting.

11. Workflow/deadline behavior

WorkflowTemplate and WorkflowStage support template stages, manual stages, contractors, subcontractors, deadlines and late detection.

12. Contractor/subcontractor behavior

ContractorReference tracks display-only and pending contractor references without creating a full supplier module.

13. Alert behavior

AlertRule and AlertEvent support record-only alert events.

No real Telegram sending.

No real CRM popup.

14. Operational report behavior

OperationalReportService produces demo projections:

client_order_history
payment_debt_summary
workflow_stage_status
alert_summary
15. Boundary confirmation

No production API added.

No web UI added.

No popup UI added.

No real Telegram notification added.

No real Calculator integration added.

No real Library integration added.

No real Accounting Registry integration added.

No real Warehouse integration added.

No real 1C sync/write added.

No real stock reservation added.

No final product/material catalog added.

16. Recommended next step

Pause after Order / Workflow / Projection Foundation v0.1 unless Blueprint approves a concrete next extension.


---