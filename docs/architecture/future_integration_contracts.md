```md
# Future Integration Contracts

Operational Registry v0.2 may include local contract-style tests for future adapters.

Allowed examples:

```text
CRM-like CreateOrderCommand can create operational order.
Gateway-like command envelope can be converted into internal command DTO.
Telegram-like source_channel can be stored as source reference.
Accounting payment reference can update operational payment_reference_confirmed status.
Calculator quote_ref can be attached as reference.

Current v0.2 does not implement real integrations.

Forbidden in v0.2:

network calls
API calls
imports from other project repositories
real CRM integration
real Gateway integration
real Telegram Bot integration
real Accounting integration
real Calculator integration
real Prepress integration

Future CRM/Gateway/Telegram integrations should be adapters around internal commands and queries.