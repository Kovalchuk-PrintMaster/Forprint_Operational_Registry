# Contact Method Policy

ContactMethod stores phones, emails, Telegram handles, Viber, web contacts and other contact values.

Contact methods are not canonical client identity.

A phone may be linked to multiple accounts through AccountContactLink.

## Raw and normalized values

Always preserve raw values:

```text
raw_value

Normalized values are additional helper fields:

normalized_value

Logic must not assume that a phone uniquely identifies a ClientAccount.


---