# Payment Projection Policy

Operational Registry may store operational payment/debt visibility.

Allowed:

```text
accounting_invoice_ref
accounting_payment_ref
one_c_document_ref
total_amount
paid_amount
unpaid_amount
payment_status
due_date
sync_confidence

Accounting Registry remains owner of accounting sync, payment truth, invoice truth and 1C posting.

Operational Registry stores projection/read model only.