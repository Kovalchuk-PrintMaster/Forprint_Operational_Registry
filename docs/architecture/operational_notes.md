```md
# Operational Notes

Operational notes are lightweight internal operational annotations.

Allowed fields:

```text
note_id
order_id
task_id optional
author_ref
note_text
visibility
created_at
metadata

Operational notes are allowed for internal order/task coordination.

They must not become:

CRM full communication history
customer chat archive
marketing notes
accounting comments as financial truth

Operational Registry may store operational notes, but CRM communication workspace and accounting
comments remain outside this module boundary.


---