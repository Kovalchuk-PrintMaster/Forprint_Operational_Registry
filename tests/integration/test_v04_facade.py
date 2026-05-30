from forprint_operational_registry.dto.commands import AddOperationalNoteCommand
from forprint_operational_registry.dto.envelope import OperationalCommandEnvelope
from forprint_operational_registry.dto.queries import GetOrderHistoryQuery, GetOrderStateQuery
from forprint_operational_registry.dto.results import (
    OperationalCommandResult,
    OperationalQueryResult,
    OperationalResultStatus,
)
from forprint_operational_registry.repositories.memory import InMemoryRepositoryBundle
from forprint_operational_registry.services.operational_registry_facade import (
    OperationalRegistryFacade,
)


def build_create_order_envelope(command_id: str = "cmd_001") -> OperationalCommandEnvelope:
    return OperationalCommandEnvelope(
        command_id=command_id,
        correlation_id="corr_001",
        idempotency_key="idem_001",
        source_module="forprint_crm_future",
        source_channel="crm_manual",
        actor_ref="operator_001",
        target_entity_type="order",
        target_entity_id="order_001",
        command_type="operational.create_order.v1",
        payload={
            "client_id": "client_001",
            "quote_ref": "quote_001",
        },
    )


def test_facade_can_create_order() -> None:
    facade = OperationalRegistryFacade(InMemoryRepositoryBundle())

    result = facade.handle_create_order(build_create_order_envelope())

    assert isinstance(result, OperationalCommandResult)
    assert result.status == OperationalResultStatus.APPLIED.value
    assert result.entity_id == "order_001"
    assert result.correlation_id == "corr_001"
    assert result.idempotency_key == "idem_001"


def test_facade_duplicate_command_returns_noop() -> None:
    facade = OperationalRegistryFacade(InMemoryRepositoryBundle())
    envelope = build_create_order_envelope()

    first_result = facade.handle_create_order(envelope)
    second_result = facade.handle_create_order(envelope)

    assert first_result.status == OperationalResultStatus.APPLIED.value
    assert second_result.status == OperationalResultStatus.NOOP.value


def test_facade_can_change_order_status() -> None:
    facade = OperationalRegistryFacade(InMemoryRepositoryBundle())
    facade.handle_create_order(build_create_order_envelope())

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
        payload={"to_status": "needs_review"},
    )

    result = facade.handle_change_order_status(envelope)

    assert result.status == OperationalResultStatus.APPLIED.value
    assert "order_status_changed" in result.events_appended


def test_facade_can_add_note() -> None:
    facade = OperationalRegistryFacade(InMemoryRepositoryBundle())
    facade.handle_create_order(build_create_order_envelope())

    result = facade.handle_add_note(
        AddOperationalNoteCommand(
            note_id="note_001",
            order_id="order_001",
            author_ref="operator_001",
            note_text="Check order.",
        ),
        command_id="cmd_note_001",
        correlation_id="corr_001",
        idempotency_key="idem_note_001",
    )

    assert result.status == OperationalResultStatus.APPLIED.value
    assert "operational_note_added" in result.events_appended


def test_facade_returns_order_state_and_history_query_results() -> None:
    facade = OperationalRegistryFacade(InMemoryRepositoryBundle())
    facade.handle_create_order(build_create_order_envelope())

    state = facade.get_order_state(GetOrderStateQuery(order_id="order_001"))
    history = facade.get_order_history(GetOrderHistoryQuery(order_id="order_001"))

    assert isinstance(state, OperationalQueryResult)
    assert isinstance(history, OperationalQueryResult)
    assert state.payload["order_id"] == "order_001"
    assert "order_created" in history.payload["events"]
