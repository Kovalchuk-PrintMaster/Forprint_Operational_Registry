# Data History and Versioning Policy

Future operational records should support history and versioning.

Recommended fields include:

```text
created_at
updated_at
valid_from
valid_to
source_system
source_ref

Mutable current state is not enough.

Operational events and historical fields should help explain how state changed.