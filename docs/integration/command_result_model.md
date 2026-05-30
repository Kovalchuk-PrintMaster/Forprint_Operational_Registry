# Command Result Model

Operational Registry v0.4 defines internal command/query results.

These models are not HTTP responses.

These models are not Gateway envelopes.

Gateway may later wrap them.

## Command result statuses

```text
accepted
applied
rejected
blocked
not_found
validation_failed
conflict
noop
Metadata preservation

Operational Registry may preserve:

command_id
correlation_id
idempotency_key
source_module
source_channel
actor_ref

Gateway may own routing and transport idempotency later.

Operational Registry does not implement global distributed idempotency in v0.4.