# Operational Fact Policy

Operational facts represent transactional or operational records.

Future examples may include:

```text
Order
OrderLine
MaterialRequirement
MaterialMovement
PaymentProjection
WorkflowStage
ProductionEvent

Facts should store:

fact_id
fact_type
business_date
client_account_id optional
source_system
source_ref optional
status

Facts must support reporting and history without becoming foreign-domain ownership.