# Persistence Safety Rules

Operational Registry may persist operational truth.

Operational Registry must not persist as owned truth:

```text
invoice/payment truth
1C snapshot
product catalog
material catalog
machine capability definition
price calculation
quote formula
prepress file lifecycle
uploaded file storage
warehouse stock/reservation truth
delivery carrier integration
CRM dashboard layout/state
Gateway routing rules
Library contract registry
architecture governance

Foreign-domain values must remain references only.

Allowed reference examples:

telegram_chat_ref
telegram_user_ref
crm_decision_ref
calculator_quote_ref
calculator_result_ref
material_consumption_estimate_ref
invoice_ref
payment_ref
prepress_job_ref
warehouse_availability_ref
library_template_ref
gateway_correlation_ref

---
