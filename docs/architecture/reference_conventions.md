id="tyrceu"
# Reference Conventions

Operational Registry may store references to foreign-domain objects.

References are identifiers only.

References are not ownership.

## Allowed references

```text
calculator_quote_ref
material_consumption_estimate_ref
invoice_ref
payment_ref
prepress_job_ref
warehouse_availability_ref
telegram_chat_ref
crm_decision_ref
library_template_ref
Boundary

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
Future source modules

Reference DTOs may name future modules as string identifiers only.

They must not import foreign module code.


---