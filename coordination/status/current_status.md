# ForPrint Operational Registry — Current Status

## Current phase

```text
client_account_card_foundation_v0_1
Last completed step
client_account_examples_lookup_terminal_preview_ready
Validation
make check: OK
tests: 138 passed
make client-card-preview: OK
Summary

Operational Registry now has the first ClientAccount Card Foundation layer:

ClientAccount
ClientGroup
ContactPerson
ContactMethod
AccountContactLink
ClientAddress
LegalEntityProfile
ClientContract
ClientBankAccount
ExternalAccountingReference
ClientPreference
ClientNote
LegacyClientImportMapping
CustomerIdentityLookupResult

Checkpoint B added:

safe demo client card examples
ambiguous phone lookup example
CustomerIdentityLookupService
terminal client card preview
make client-card-preview
Boundaries

No production API added.

No real 1C sync added.

No CRM dashboard added.

No Telegram runtime integration added.

No Calculator integration added.

No Library integration added.

No warehouse stock truth added.

Phone remains a lookup key, not canonical identity.

Canonical customer/account truth remains:

client_account_id

---

## Data Foundation Strategy v0.1

Operational Registry now has policy/base abstractions for future operational data modeling.

Added concepts:

```text
MasterDataRecord
OperationalFactRecord
OperationalEventRecord
ExternalReference
DataProjection
ReportDefinition
RawNormalizedValue

Added terminal preview:

make data-foundation-preview

Boundary:

No real product card.
No real material catalog.
No real supplier card.
No real accounting sync.
No real 1C write.
No production API.
No web UI.
No Telegram notification.
No Calculator runtime integration.
No Warehouse stock truth.

---

## Order / Workflow / Projection Foundation v0.1

Operational Registry now has flexible order/workflow/projection foundation models.

Added concepts:

```text
OperationalOrder
OperationalOrderLine
CalculatorOutputPackageReference
ProductServiceReference
MaterialRequirement
PaymentProjection
WorkflowTemplate
WorkflowStage
ContractorReference
DeadlineControlRecord
AlertRule
AlertEvent
OperationalReportService

Added terminal previews:

make order-preview
make workflow-preview
make payment-preview
make material-requirement-preview
make alert-preview
make operational-report-preview

Boundary:

No production API.
No web UI.
No popup UI.
No real Telegram notification.
No real Calculator integration.
No real Library integration.
No real Accounting Registry integration.
No real Warehouse integration.
No real 1C sync/write.
No real stock reservation.
No final product/material catalog.

---

## Canonical Dictionary Mapping v0.1

Operational Registry now has a semantic alignment layer for Library shared operational dictionaries.

Added:

```text
CanonicalDictionaryReference
LocalEnumMapping
DictionaryVersionPin
DictionaryAlignmentResult
dictionary mapping config
dictionary mapping validator
dictionary mapping preview

Boundary:

No Library dictionary edits.
No runtime Library integration.
No product/material catalog.
No production API.
No web UI.
No Telegram notification.
No 1C sync/write.