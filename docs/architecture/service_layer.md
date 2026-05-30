```md
# Service Layer

Operational Registry v0.2 adds internal service/use-case classes.

Approved services:

```text
ClientRegistryService
OrderRegistryService
TaskRegistryService
OperationalEventService
OperationalNoteService
OrderQueryService
OrderHistoryQueryService

Responsibilities:

ClientRegistryService = create/read operational client identity.
OrderRegistryService = create order and change operational status.
TaskRegistryService = create/assign/update operational tasks.
OperationalEventService = append operational events.
OperationalNoteService = add lightweight operational notes.
OrderQueryService = read current order state.
OrderHistoryQueryService = read append-only operational history.

The service layer is internal.

It must not expose production API in v0.2.