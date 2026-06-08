# ClientAccount Card Foundation

Operational Registry owns the internal ClientAccount foundation.

The canonical customer/account truth is:

```text
client_account_id

Not phone number.

Not Telegram username.

Not human display name.

Not 1C/BAS code.

Normalized direction

ForPrint must not use a flat clients table as final customer truth.

The correct foundation is:

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
Boundary

Operational Registry owns operational customer/account identity and related operational records.

Operational Registry does not own:

canonical product/material/service semantics
Calculator pricing logic
1C live synchronization
real accounting posting
CRM dashboard
Telegram runtime UI
prepress file lifecycle
warehouse stock truth

---