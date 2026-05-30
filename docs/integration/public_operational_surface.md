# Public Operational Surface

Operational Registry exposes internal operational command/query shapes.

It does not expose production API.

Other modules may design against:

```text
command shapes
query shapes
result shapes
projection shapes
reference conventions
handoff examples
error taxonomy
status export
adapter boundary docs
Future module expectations

Telegram Bot may later prepare order intake drafts.

CRM may later command operational actions and show dashboards.

Gateway may later transport validated commands.

Calculator may later provide quote/calculation references.

Accounting Registry may later provide invoice/payment references.

Prepress Hub may later provide prepress job/status references.

Library will later own canonical contracts/templates/catalogs.

Refusal boundary

Operational Registry refuses to own:

invoice/payment truth
product/material catalog truth
calculation logic
prepress file lifecycle
warehouse stock truth
CRM dashboard layout/state
Gateway routing rules
Library contract registry