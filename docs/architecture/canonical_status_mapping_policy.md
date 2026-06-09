# Canonical Status Mapping Policy

Operational Registry may keep local draft enum values temporarily.

Each local value must be explicitly classified as one of:

```text
mapped to Library canonical ID
pending Library reference
intentionally local/deferred
deprecated reference
manual review required
unresolved
unknown

No silent untracked local status drift is allowed.

Ownership

ForPrint Library owns canonical dictionary IDs.

Operational Registry consumes or references Library dictionary IDs.

Operational Registry must not define final canonical statuses when Library already owns the dictionary group.

Machine values

Dictionary IDs are machine-stable values.

Labels are display-layer values.

Deprecated Library values remain readable but must be marked as deprecated references.

Unknown local values require manual review.


---