```md
# Operational Blockers

Operational blockers are lightweight operational readiness helpers.

They help answer:

```text
Is this order/task operationally blocked right now?

They do not answer:

What is the real payment truth?
What is the warehouse stock truth?
What is the prepress file lifecycle?
What is the CRM communication history?
Allowed blocker types
missing_client_data
missing_calculation
waiting_payment_reference
waiting_prepress_check
waiting_operator_review
material_availability_unknown
manual_review_required
Boundary

OperationalBlocker may store operational state and references.

OperationalBlocker must not become:

Accounting payment truth
Warehouse reservation truth
Prepress file lifecycle
CRM communication history

Blocker creation and resolution append OperationalEvent records.

This is not a full workflow engine.


---