# Repository Storage Boundary

Operational Registry services depend on repository interfaces.

Allowed repository backends in v0.5:

```text
memory
sqlite

Planned future backend:

postgresql

Services, facade and projections should use repository bundles, not database-specific code.

Other modules must not directly read or write Operational Registry tables.