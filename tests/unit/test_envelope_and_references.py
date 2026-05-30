import pytest
from forprint_operational_registry.dto.envelope import OperationalCommandEnvelope
from forprint_operational_registry.dto.references import (
    AccountingReference,
    CalculatorReference,
    CRMReference,
    ExternalReference,
    GatewayReference,
    LibraryReference,
    PrepressReference,
    TelegramReference,
)


def test_operational_command_envelope_can_be_created() -> None:
    envelope = OperationalCommandEnvelope(
        command_id="cmd_001",
        correlation_id="corr_001",
        idempotency_key="idem_001",
        source_module="forprint_crm_future",
        source_channel="crm_manual",
        actor_ref="operator_001",
        target_entity_type="order",
        target_entity_id="order_001",
        command_type="operational.create_order.v1",
        payload={"client_id": "client_001"},
    )

    assert envelope.command_id == "cmd_001"
    assert envelope.payload["client_id"] == "client_001"


def test_envelope_payload_is_immutable() -> None:
    envelope = OperationalCommandEnvelope(
        command_id="cmd_001",
        correlation_id="corr_001",
        idempotency_key="idem_001",
        source_module="forprint_crm_future",
        source_channel="crm_manual",
        actor_ref="operator_001",
        target_entity_type="order",
        target_entity_id="order_001",
        command_type="operational.create_order.v1",
        payload={"client_id": "client_001"},
    )

    with pytest.raises(TypeError):
        envelope.payload["client_id"] = "changed"


def test_envelope_can_convert_to_create_order_command() -> None:
    envelope = OperationalCommandEnvelope(
        command_id="cmd_001",
        correlation_id="corr_001",
        idempotency_key="idem_001",
        source_module="forprint_crm_future",
        source_channel="telegram_bot",
        actor_ref="operator_001",
        target_entity_type="order",
        target_entity_id="order_001",
        command_type="operational.create_order.v1",
        payload={
            "client_id": "client_001",
            "quote_ref": "quote_001",
            "accounting_refs": {"invoice_ref": "invoice_001"},
        },
    )

    command = envelope.to_create_order_command()

    assert command.order_id == "order_001"
    assert command.client_id == "client_001"
    assert command.source_channel == "telegram_bot"
    assert command.quote_ref == "quote_001"
    assert command.accounting_refs["invoice_ref"] == "invoice_001"


def test_envelope_can_convert_to_change_order_status_command() -> None:
    envelope = OperationalCommandEnvelope(
        command_id="cmd_002",
        correlation_id="corr_001",
        idempotency_key="idem_002",
        source_module="forprint_crm_future",
        source_channel="crm_manual",
        actor_ref="operator_001",
        target_entity_type="order",
        target_entity_id="order_001",
        command_type="operational.change_order_status.v1",
        payload={"to_status": "needs_review", "reason": "Manual review requested."},
    )

    command = envelope.to_change_order_status_command()

    assert command.order_id == "order_001"
    assert command.to_status == "needs_review"
    assert command.reason == "Manual review requested."


def test_reference_dtos_can_be_created_without_foreign_objects() -> None:
    references = (
        ExternalReference(
            reference_id="external_001",
            reference_type="generic",
            source_module="external_future",
        ),
        AccountingReference(reference_id="invoice_001", reference_type="invoice_ref"),
        CalculatorReference(reference_id="quote_001", reference_type="quote_ref"),
        PrepressReference(reference_id="prepress_001", reference_type="prepress_job_ref"),
        GatewayReference(reference_id="corr_001", reference_type="correlation_ref"),
        TelegramReference(reference_id="chat_001", reference_type="telegram_chat_ref"),
        CRMReference(reference_id="decision_001", reference_type="crm_decision_ref"),
        LibraryReference(reference_id="template_001", reference_type="library_template_ref"),
    )

    assert references[1].source_module == "accounting_registry_future"
    assert references[2].source_module == "calculator_engine_future"
    assert references[5].source_channel == "telegram_bot"
