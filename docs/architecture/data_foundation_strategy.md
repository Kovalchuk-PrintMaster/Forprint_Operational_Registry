# Data Foundation Strategy

Operational Registry must become a strong internal operational data foundation, not an Excel-like list of customers.

This step defines policies and base abstractions only.

It does not create real product, material, supplier or accounting catalogs.

## Foundation concepts

```text
MasterDataRecord
OperationalFactRecord
OperationalEventRecord
ExternalReference
DataProjection
ReportDefinition
Rule

Future entities must be based on:

real ForPrint business scenarios
1C/BAS compatibility where accounting-relevant
stable internal IDs
external references
raw imported values
normalized values
version/history fields
clear module ownership boundaries