import pytest
from forprint_operational_registry.models.order import OrderRecord
from forprint_operational_registry.models.status import ensure_allowed_order_status
from forprint_operational_registry.services.order_lifecycle import (
    InvalidOrderTransition,
    get_allowed_order_transitions,
    is_valid_transition,
    transition_order_status,
    validate_order_transition,
)


def test_valid_lifecycle_transition_is_accepted() -> None:
    validate_order_transition("new", "needs_review")

    assert is_valid_transition("new", "needs_review") is True
    assert "needs_review" in get_allowed_order_transitions("new")


def test_invalid_lifecycle_transition_is_rejected() -> None:
    with pytest.raises(InvalidOrderTransition):
        validate_order_transition("new", "completed")

    assert is_valid_transition("new", "completed") is False


def test_status_change_appends_operational_event() -> None:
    order = OrderRecord(order_id="order_001", client_id="client_001")

    event = transition_order_status(
        order=order,
        to_status="needs_review",
        actor_ref="operator_001",
    )

    assert order.order_status == "needs_review"
    assert event.event_type == "order_status_changed"
    assert event.payload["from_status"] == "new"
    assert event.payload["to_status"] == "needs_review"


def test_payment_reference_confirmed_is_allowed_and_paid_is_not() -> None:
    assert ensure_allowed_order_status("payment_reference_confirmed")

    with pytest.raises(ValueError, match="forbidden"):
        ensure_allowed_order_status("paid")
