```md
# Module Reference Conventions

Operational Registry may store references to foreign-domain objects.

References are strings, DTOs or snapshots only.

Operational Registry must not import foreign objects.

Operational Registry must not own foreign truth.

## Approved reference fields

```text
telegram_chat_ref
telegram_user_ref
crm_decision_ref
calculator_quote_ref
calculator_result_ref
material_consumption_estimate_ref
accounting_invoice_ref
accounting_payment_ref
prepress_job_ref
prepress_result_ref
warehouse_availability_ref
library_template_ref
gateway_correlation_ref
Boundary

Operational Registry may use references for operational workflow decisions.

Operational Registry must not own:

price_calculation
quote formula
invoice/payment truth
1C snapshot
product catalog
material catalog
machine capability definition
prepress file lifecycle
uploaded file storage
warehouse stock/reservation truth
delivery carrier integration
CRM dashboard layout/state
Gateway routing rules
Library contract registry
architecture governance