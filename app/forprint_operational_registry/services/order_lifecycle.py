"""Generic order lifecycle service for Operational Registry v0.1."""

from datetime import UTC, datetime
from typing import Protocol
from uuid import uuid4

from forprint_operational_registry.models.event import OperationalEvent
from forprint_operational_registry.models.order import OrderRecord
from forprint_operational_registry.models.status import ensure_allowed_order_status


class InvalidOrderTransition(ValueError):
    """Raised when order status transition is not allowed."""


class SupportsOrderEvents(Protocol):
    """Minimal protocol for repositories that can append order events."""

    def append_order_event(self, event: OperationalEvent) -> None:
        """Append order event to history."""


GENERIC_ORDER_LIFECYCLE_V0: dict[str, set[str]] = {
    "new": {"needs_review", "quote_pending", "blocked", "cancelled"},
    "needs_review": {"quote_pending", "blocked", "cancelled"},
    "quote_pending": {"quote_accepted", "needs_review", "blocked", "cancelled"},
    "quote_accepted": {"payment_reference_pending", "blocked", "cancelled"},
    "payment_reference_pending": {
        "payment_reference_confirmed",
        "needs_review",
        "blocked",
        "cancelled",
    },
    "payment_reference_confirmed": {"in_prepress", "ready_for_production", "blocked", "cancelled"},
    "in_prepress": {"ready_for_production", "needs_review", "blocked", "cancelled"},
    "ready_for_production": {"in_production", "blocked", "cancelled"},
    "in_production": {"ready_for_pickup", "blocked", "cancelled"},
    "ready_for_pickup": {"completed", "blocked", "cancelled"},
    "blocked": {"needs_review", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}


def is_valid_transition(from_status: str, to_status: str) -> bool:
    """Return whether a generic v0.1 status transition is allowed."""

    ensure_allowed_order_status(from_status)
    ensure_allowed_order_status(to_status)

    return to_status in GENERIC_ORDER_LIFECYCLE_V0[from_status]


def transition_order_status(
    order: OrderRecord,
    to_status: str,
    actor_ref: str,
    source_module: str = "forprint_operational_registry",
    repository: SupportsOrderEvents | None = None,
) -> OperationalEvent:
    """Transition order status and append an immutable OperationalEvent."""

    from_status = order.order_status

    if not is_valid_transition(from_status, to_status):
        raise InvalidOrderTransition(f"Invalid order transition: {from_status} -> {to_status}")

    order.order_status = to_status
    order.workflow_status = to_status
    order.updated_at = datetime.now(UTC)

    event = OperationalEvent(
        event_id=f"evt_{uuid4().hex}",
        entity_type="order",
        entity_id=order.order_id,
        event_type="order_status_changed",
        actor_ref=actor_ref,
        source_module=source_module,
        payload={
            "from_status": from_status,
            "to_status": to_status,
            "lifecycle": "generic_v0",
        },
    )

    if repository is not None:
        repository.append_order_event(event)

    return event
