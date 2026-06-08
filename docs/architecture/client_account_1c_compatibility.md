# ClientAccount 1C/BAS Compatibility

ForPrint internal DB is the main internal operational source.

1C/BAS codes and refs must be stored as external accounting references.

They are not ForPrint primary IDs.

## Rule

```text
ForPrint primary identity = client_account_id
1C/BAS identity = ExternalAccountingReference
Mapping direction

1C/BAS counterparty/contact/address/contract/bank account structures are mapped into normalized ForPrint structures.

They are not copied blindly.

Raw 1C/BAS presentations must be preserved:

raw_name
raw_phone
raw_address
raw_contact_info_presentation
raw_comment
raw_1c_code
legacy_source_id
Deferred

No live 1C write.

No production accounting sync.

No real Accounting Registry adapter in this step.


---