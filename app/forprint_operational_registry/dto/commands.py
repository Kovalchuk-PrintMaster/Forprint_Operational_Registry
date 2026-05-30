"""Internal command DTOs for Operational Registry v0.2.

DTOs are transport-agnostic.
They do not depend on Telegram, CRM, Gateway, HTTP or any external module runtime.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class CreateClientCommand:
    """Create canonical operational client identity."""

    client_id: str
    display_name: str
    contact_refs: tuple[str, ...] = ()
    source_refs: dict[str, Any] = field(default_factory=dict)
    status: str = "active"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CreateOrderCommand:
    """Create canonical operational order state.

    Foreign-domain data must be passed as references only.
    """

    order_id: str
    client_id: str
    source_channel: str
    source_refs: dict[str, Any] = field(default_factory=dict)
    quote_ref: str | None = None
    calculator_result_ref: str | None = None
    accounting_refs: dict[str, Any] = field(default_factory=dict)
    production_refs: dict[str, Any] = field(default_factory=dict)
    prepress_refs: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    actor_ref: str = "system"
    source_module: str = "forprint_operational_registry"


@dataclass(frozen=True, slots=True)
class ChangeOrderStatusCommand:
    """Change operational order status."""

    order_id: str
    to_status: str
    actor_ref: str
    source_module: str = "forprint_operational_registry"
    reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CreateOperationalTaskCommand:
    """Create operational task attached to an order."""

    task_id: str
    order_id: str
    task_type: str
    assigned_to_ref: str | None = None
    deadline: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    actor_ref: str = "system"
    source_module: str = "forprint_operational_registry"


@dataclass(frozen=True, slots=True)
class AssignOperationalTaskCommand:
    """Assign existing operational task."""

    task_id: str
    assigned_to_ref: str
    actor_ref: str
    source_module: str = "forprint_operational_registry"


@dataclass(frozen=True, slots=True)
class ChangeTaskStatusCommand:
    """Change operational task status."""

    task_id: str
    to_status: str
    actor_ref: str
    source_module: str = "forprint_operational_registry"


@dataclass(frozen=True, slots=True)
class AddOperationalNoteCommand:
    """Add lightweight operational note."""

    note_id: str
    order_id: str
    author_ref: str
    note_text: str
    task_id: str | None = None
    visibility: str = "internal"
    metadata: dict[str, Any] = field(default_factory=dict)
    source_module: str = "forprint_operational_registry"


@dataclass(frozen=True, slots=True)
class AppendOperationalEventCommand:
    """Append operational event directly through internal service."""

    event_id: str
    entity_type: str
    entity_id: str
    event_type: str
    actor_ref: str
    source_module: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class CreateOperationalBlockerCommand:
    """Create lightweight operational blocker."""

    blocker_id: str
    entity_type: str
    entity_id: str
    blocker_type: str
    reason: str
    source_module: str = "forprint_operational_registry"
    severity: str = "medium"
    metadata: dict[str, Any] = field(default_factory=dict)
    actor_ref: str = "system"


@dataclass(frozen=True, slots=True)
class ResolveOperationalBlockerCommand:
    """Resolve lightweight operational blocker."""

    blocker_id: str
    actor_ref: str
    source_module: str = "forprint_operational_registry"
    reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
