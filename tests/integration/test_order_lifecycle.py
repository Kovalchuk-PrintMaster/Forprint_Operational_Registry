import pytest
from forprint_operational_registry.models.order import OrderRecord
from forprint_operational_registry.services.order_lifecycle import (
    InvalidOrderTransition,
    transition_order_status,
)
from forprint_operational_registry.storage.memory import InMemoryOperationalRegistry


def test_valid_order_lifecycle_transition_appends_event() -> None:
    registry = InMemoryOperationalRegistry()
    order = OrderRecord(order_id="order_001", client_id="client_001")
    registry.add_order(order)

    event = transition_order_status(
        order=order,
        to_status="needs_review",
        actor_ref="operator_001",
        repository=registry,
    )

    assert order.order_status == "needs_review"
    assert event.payload["from_status"] == "new"
    assert event.payload["to_status"] == "needs_review"
    assert registry.list_order_events("order_001") == (event,)


def test_invalid_order_lifecycle_transition_is_rejected() -> None:
    order = OrderRecord(order_id="order_001", client_id="client_001")

    with pytest.raises(InvalidOrderTransition):
        transition_order_status(
            order=order,
            to_status="completed",
            actor_ref="operator_001",
        )


def test_status_transition_creates_new_event_without_mutating_existing_event() -> None:
    registry = InMemoryOperationalRegistry()
    order = OrderRecord(order_id="order_001", client_id="client_001")
    registry.add_order(order)

    first_event = transition_order_status(
        order=order,
        to_status="needs_review",
        actor_ref="operator_001",
        repository=registry,
    )

    first_payload_before = dict(first_event.payload)

    second_event = transition_order_status(
        order=order,
        to_status="quote_pending",
        actor_ref="operator_001",
        repository=registry,
    )

    assert dict(first_event.payload) == first_payload_before
    assert len(registry.list_order_events("order_001")) == 2
    assert first_event != second_event
