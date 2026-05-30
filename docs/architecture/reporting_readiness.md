```md
# Reporting Readiness

Operational Registry v0.3 adds local module status export for future Project Inspector readiness.

The export is local/offline.

It is not a Project Inspector integration.

It may include:

```text
module_id
module_status
implemented_layers
owned_objects
must_not_own
checks_summary
docs_summary
open_questions
last_generated_at

The export must not include foreign runtime data.

Generated reports are written to reports/ and ignored by Git.