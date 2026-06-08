# Master Data Policy

Master data represents stable reference entities.

Future examples may include:

```text
ClientAccount
Product
Service
Material
Supplier
Contractor
WarehouseItem
OperationType

This document does not create these catalogs.

ID rule
internal_id is logic truth
display_name is user-facing and editable
raw_source_name preserves imported value

Human names, 1C codes and phone numbers must not become primary IDs.