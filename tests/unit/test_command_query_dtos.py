from forprint_operational_registry.dto.commands import (
    AddOperationalNoteCommand,
    CreateClientCommand,
    CreateOrderCommand,
)
from forprint_operational_registry.dto.queries import GetOrderHistoryQuery, GetOrderStateQuery


def test_create_client_command_is_plain_dto() -> None:
    command = CreateClientCommand(
        client_id="client_001",
        display_name="Test Client",
        contact_refs=("telegram:user:1",),
    )

    assert command.client_id == "client_001"
    assert command.contact_refs == ("telegram:user:1",)


def test_create_order_command_uses_references_only() -> None:
    command = CreateOrderCommand(
        order_id="order_001",
        client_id="client_001",
        source_channel="telegram_bot",
        quote_ref="quote_001",
        calculator_result_ref="calc_result_001",
        accounting_refs={"invoice_ref": "invoice_001"},
        prepress_refs={"prepress_task_ref": "prepress_001"},
    )

    assert command.quote_ref == "quote_001"
    assert command.accounting_refs["invoice_ref"] == "invoice_001"
    assert "payment_object" not in command.accounting_refs


def test_note_and_query_dtos_can_be_created() -> None:
    note_command = AddOperationalNoteCommand(
        note_id="note_001",
        order_id="order_001",
        author_ref="operator_001",
        note_text="Check layout before production.",
    )

    state_query = GetOrderStateQuery(order_id="order_001")
    history_query = GetOrderHistoryQuery(order_id="order_001")

    assert note_command.visibility == "internal"
    assert state_query.order_id == "order_001"
    assert history_query.order_id == "order_001"
