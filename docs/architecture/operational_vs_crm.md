```md
# Operational Registry vs CRM

CRM coordinates workflows and displays dashboards.

Operational Registry stores canonical operational truth.

## Correct relationship

```text
CRM displays and coordinates.
Operational Registry stores operational truth.

CRM may request actions:

create order
update order status
assign task
add operational note
request manual review

The canonical resulting operational state belongs to Operational Registry.

ClientRecord boundary

In v0.1:

ClientRecord = operational client identity

Allowed fields:

client_id
display_name
contact_refs
source_refs
status
metadata
created_at
updated_at

Forbidden in v0.1:

full CRM interaction history
sales pipeline
marketing profile
CRM dashboard preferences
manager workspace state
full communication timeline

Future CRM may own:

ClientWorkspace
CRMClientProjection
ClientProfileView
SavedClientView
ClientCommunicationWorkspace

---