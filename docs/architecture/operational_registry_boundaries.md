# Operational Registry Boundaries

ForPrint Operational Registry owns canonical operational truth.

It answers:

```text
What is the canonical operational state of this client/order/task/status right now?

It does not answer:

What is the invoice/payment truth?
What is the product/material canonical definition?
How should the price be calculated?
How should files be processed?
How should user dashboard look?
How should routing be done?
Module boundaries

Operational Registry owns:

client_record
order
order_status
workflow_state
operational_task
task_status
operational_event
order_history_event
manual_decision_record
operator_action_record
operational_note
deadline
responsible_user_reference

Operational Registry must not own:

invoice
payment
accounting_document
material_catalog
product_catalog
price_calculation
prepress_file_lifecycle
uploaded_file_binary_storage
warehouse_stock_balance
delivery_carrier_integration
integration_routing
library_contract_registry
architecture_governance
System separation
Operational Registry owns operational truth.
CRM coordinates and displays.
Accounting owns accounting/1C truth.
Library owns catalogs/contracts.
Gateway routes runtime commands later.
Calculator calculates.
Prepress processes files.

v0.1 must stay small, testable and boundary-safe.


---