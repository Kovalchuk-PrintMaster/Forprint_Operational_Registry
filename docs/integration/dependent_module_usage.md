# Dependent Module Usage

After v0.4, dependent modules may safely reference Operational Registry shapes.

## Telegram Bot

May prepare an order intake draft that maps to a future create order command.

## CRM

May design workflow actions around Operational Registry command/result shapes.

## Gateway

May design future transport around command envelopes and results.

## Calculator

May provide quote/calculation references only.

## Accounting Registry

May provide invoice/payment references only.

## Prepress Hub

May provide prepress job/status references only.

## Boundary

No dependent module should assume direct write access or real runtime integration yet.