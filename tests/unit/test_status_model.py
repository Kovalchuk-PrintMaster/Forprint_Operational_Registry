import pytest
from forprint_operational_registry.models.status import (
    ORDER_STATUSES,
    RECOMMENDED_SOURCE_CHANNELS,
    ensure_allowed_order_status,
)


def test_payment_reference_confirmed_is_allowed() -> None:
    assert (
        ensure_allowed_order_status("payment_reference_confirmed") == "payment_reference_confirmed"
    )


def test_paid_is_forbidden() -> None:
    with pytest.raises(ValueError, match="forbidden"):
        ensure_allowed_order_status("paid")


def test_v0_lifecycle_statuses_are_generic() -> None:
    assert "payment_reference_pending" in ORDER_STATUSES
    assert "payment_reference_confirmed" in ORDER_STATUSES
    assert "in_prepress" in ORDER_STATUSES
    assert "completed" in ORDER_STATUSES


def test_recommended_source_channels_are_available_without_hard_enum() -> None:
    assert "telegram_bot" in RECOMMENDED_SOURCE_CHANNELS
    assert "mobile_app" in RECOMMENDED_SOURCE_CHANNELS
