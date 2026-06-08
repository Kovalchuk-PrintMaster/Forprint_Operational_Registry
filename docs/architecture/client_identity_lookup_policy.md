# Client Identity Lookup Policy

Client identity is based on stable internal ClientAccount ID.

```text
client_account_id = canonical truth

Phone is a strong lookup key but not canonical identity.

One phone may match multiple ClientAccounts.

When multiple accounts match, Operational Registry must not auto-select.

It should return:

multiple_matches_manual_review_required
Lookup statuses
single_match
multiple_matches_manual_review_required
no_match
invalid_lookup_input
Future routing

Ambiguous matches should later route to operator/manual account selection.


---