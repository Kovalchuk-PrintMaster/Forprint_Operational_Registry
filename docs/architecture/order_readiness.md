```md
# Order Readiness

OrderReadinessService evaluates internal operational readiness.

It may detect:

```text
active blockers
missing calculation reference
waiting payment reference
manual review required
waiting prepress check
material availability unknown

It must not:

check real payment balance
check real warehouse stock
run Calculator
run Prepress
call Gateway
call CRM

Readiness is based only on Operational Registry state and stored references.


---