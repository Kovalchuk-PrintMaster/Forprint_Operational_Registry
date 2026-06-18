# Local Readiness Checklist

## Required repository state

- [ ] Repository working tree is clean before starting local validation.
- [ ] Blueprint repository is pulled with `git pull --ff-only`.
- [ ] Current Blueprint commit is acknowledged.
- [ ] Operational Registry is on the expected branch.
- [ ] No accidental generated report diffs are present.

## Blueprint visibility

- [ ] `make blueprint-instruction-check` passes.
- [ ] `make blueprint-standards-check` passes.
- [ ] `make blueprint-instruction-sync` is idempotent.
- [ ] `make blueprint-standards-sync` is idempotent.
- [ ] Repeated sync does not create timestamp-only git diffs.

## Validation

- [ ] `make check-report` passes.
- [ ] `make check` passes.
- [ ] `make governance-check` passes.
- [ ] Pytest passes with the current expected test count or higher.
- [ ] Ruff lint passes.
- [ ] Local previews used by check-report pass.

## Safe local data

- [ ] Examples use safe local fixtures only.
- [ ] No real customer production data is required.
- [ ] No real accounting data is required.
- [ ] No real 1C export/import data is required.
- [ ] No secrets, tokens or credentials are stored in fixtures.

## Runtime boundaries

- [ ] No production API was added.
- [ ] No live external integration was added.
- [ ] No real 1C sync/write was added.
- [ ] No automatic posting was added.
- [ ] No CRM dashboard was added.
- [ ] No Telegram runtime UI was added.
- [ ] No Calculator final price ownership was added.
- [ ] No Library catalog ownership was added.
- [ ] No Warehouse stock truth was added.
- [ ] No Prepress lifecycle ownership was added.

## Coordination readiness

- [ ] `coordination/status/current_status.yaml` is current.
- [ ] `coordination/reports/index.yaml` references the current completion report.
- [ ] Completion report exists for the current phase.
- [ ] Instruction sources reviewed are recorded.
- [ ] Standards reviewed are recorded.
- [ ] Standards alignment notes are recorded.
- [ ] Boundary confirmation is recorded.

## Local launch readiness result

The module may be considered locally launch-ready only when all required validation and boundary checks are green.