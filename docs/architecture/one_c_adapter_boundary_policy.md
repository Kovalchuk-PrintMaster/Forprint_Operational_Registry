# 1C/BAS Adapter Boundary Policy

ForPrint DB should be modern and internal-first.

1C/BAS compatibility is required, but handled through references and adapters.

Do not degrade the internal model only to match 1C.

Accounting Registry will later own:

```text
1C import workflows
1C export workflows
sync status workflows
accounting posting workflows

Operational Registry stores sync-friendly references.

No live 1C write in this step.

No production accounting sync in this step.