```md
# Operational Registry vs Accounting Registry

Operational Registry owns operational order/client/task state.

Accounting Registry owns invoice, payment, accounting document and 1C truth.

## Operational Registry may own

```text
order_id
client_id
order_status
workflow_status
production readiness
task assignment
operational history
Accounting Registry owns
invoice_id
payment_id
payment_status
invoice_status
accounting_document
1C snapshot
1C reconciliation
Payment terminology decision

Operational Registry must not use paid as canonical payment truth.

Allowed operational statuses:

payment_reference_pending
payment_reference_confirmed

Meaning:

Operational workflow received/confirmed a payment reference from Accounting Registry.

Forbidden meaning:

Operational Registry is the canonical source of payment truth.

Operational Registry may store references only:

invoice_ref
payment_ref
accounting_document_ref
payment_status_reference

---