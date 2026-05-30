# Lifecycle Validation

Operational Registry v0.3 hardens generic lifecycle validation.

The lifecycle remains generic.

It is not a full workflow engine.

It is not product-specific.

Future lifecycle may become template-driven by ForPrint Library workflow/product definitions.

## Order statuses

```text
new
needs_review
quote_pending
quote_accepted
payment_reference_pending
payment_reference_confirmed
in_prepress
ready_for_production
in_production
ready_for_pickup
completed
cancelled
blocked
Payment boundary

Do not use paid as canonical Operational Registry status.

Allowed:

payment_reference_pending
payment_reference_confirmed

Meaning:

Operational workflow received or confirmed a payment reference.

Accounting Registry owns actual payment truth.

Transition validation

Valid lifecycle transitions are accepted.

Invalid lifecycle transitions are rejected.

Terminal states cannot transition further:

completed
cancelled

Status changes append OperationalEvent records.


# 11. Онови check validations

У `app/forprint_operational_registry/services/registry_checks.py`:

## 11.1 Додай docs у `REQUIRED_DOCS`

Додай:

```python
"docs/architecture/lifecycle_validation.md",
"docs/architecture/operational_blockers.md",