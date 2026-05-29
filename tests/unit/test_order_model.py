import pytest
from forprint_operational_registry.models.order import OrderRecord


def test_order_record_can_be_created() -> None:
    order = OrderRecord(
        order_id="order_001",
        client_id="client_001",
        source_channel="telegram_bot",
        quote_ref="quote_001",
        accounting_refs={"invoice_ref": "invoice_001"},
    )

    assert order.order_id == "order_001"
    assert order.order_status == "new"
    assert order.quote_ref == "quote_001"


def test_source_channel_remains_flexible_string() -> None:
    order = OrderRecord(
        order_id="order_001",
        client_id="client_001",
        source_channel="future_channel_from_gateway",
    )

    assert order.source_channel == "future_channel_from_gateway"


def test_paid_status_is_rejected() -> None:
    with pytest.raises(ValueError, match="forbidden"):
        OrderRecord(
            order_id="order_001",
            client_id="client_001",
            order_status="paid",
        )
