# Material Requirement Policy

Operational Registry may store planned material requirements and projections.

This is not warehouse stock truth.

Allowed:

```text
material_display_name
raw_material_name
quantity_planned
quantity_confirmed
library_material_id optional
warehouse_reference optional
requirement_status

Warehouse module will later own actual stock and reservation truth.

Operational Registry stores planning/projection only.