```md
# Order Lifecycle v0

Operational Registry v0.1 uses one simple generic order lifecycle.

## Initial generic statuses

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
Important payment rule

Do not use paid as a canonical Operational Registry status.

Use:

payment_reference_pending
payment_reference_confirmed

Accounting Registry owns real payment truth.

source_channel rule

In v0.1, source_channel remains a flexible string.

Recommended values:

telegram_bot
website
mobile_app
crm_manual
gateway_import
internal_module
legacy_import

A hard enum is intentionally deferred because Gateway, Website, Telegram Bot and Mobile App contracts are not fully stabilized yet.

Append-only event rule

OperationalEvent is append-only by design.

Required rule:

State changes create new OperationalEvent records.
Existing events are not edited in place.

v0.1 implements this through:

model
service behavior
tests
documentation
Future lifecycle direction

v0.1 uses a generic lifecycle.

Future order lifecycle may depend on product/workflow templates from ForPrint Library.

Future architecture:

v0.1 = generic lifecycle
future = template-driven lifecycle based on Library workflow/product definitions

The v0.1 lifecycle must not be hardcoded so deeply that Library-driven workflow templates become impossible later.


---