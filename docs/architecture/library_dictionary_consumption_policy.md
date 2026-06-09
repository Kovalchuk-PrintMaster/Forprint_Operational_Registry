# Library Dictionary Consumption Policy

ForPrint Library owns canonical shared dictionary IDs.

Operational Registry consumes/reference these IDs.

Operational Registry must not edit Library dictionaries.

Dictionary labels are display-layer values.

Dictionary IDs are machine-stable values.

No runtime Library dependency is required in this step.
docs/architecture/canonical_status_mapping_policy.md
# Canonical Status Mapping Policy

Operational Registry may keep local draft enum values temporarily.

Each local value must be:

```text
mapped to Library canonical ID
pending mapping
intentionally local/deferred
deprecated
manual review required
unresolved

No silent untracked local status drift is allowed.