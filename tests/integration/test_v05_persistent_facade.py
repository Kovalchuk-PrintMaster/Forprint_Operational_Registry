from pathlib import Path

from forprint_operational_registry.dto.envelope import OperationalCommandEnvelope
from forprint_operational_registry.dto.queries import GetOrderStateQuery
from forprint_operational_registry.dto.results import OperationalResultStatus
from forprint_operational_registry.repositories.sqlite import SQLiteRepositoryBundle
from forprint_operational_registry.services.operational_registry_facade import (
    OperationalRegistryFacade,
)
from forprint_operational_registry.services.projections import OperationalProjectionService


def build_envelope() -> OperationalCommandEnvelope:
    return OperationalCommandEnvelope(
        command_id="cmd_001",
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


def test_facade_can_operate_against_sqlite_repository_bundle(tmp_path: Path) -> None:
    bundle = SQLiteRepositoryBundle(tmp_path / "facade.sqlite3")
    facade = OperationalRegistryFacade(bundle)

    result = facade.handle_create_order(build_envelope())

    assert result.status == OperationalResultStatus.APPLIED.value
    assert bundle.orders.get("order_001").quote_ref == "quote_001"


def test_order_state_query_works_against_sqlite_bundle(tmp_path: Path) -> None:
    bundle = SQLiteRepositoryBundle(tmp_path / "facade.sqlite3")
    facade = OperationalRegistryFacade(bundle)
    facade.handle_create_order(build_envelope())

    result = facade.get_order_state(GetOrderStateQuery(order_id="order_001"))

    assert result.payload["order_id"] == "order_001"
    assert result.payload["quote_ref"] == "quote_001"


def test_projection_can_be_generated_from_persistent_data(tmp_path: Path) -> None:
    bundle = SQLiteRepositoryBundle(tmp_path / "projection.sqlite3")
    facade = OperationalRegistryFacade(bundle)
    facade.handle_create_order(build_envelope())

    projection = OperationalProjectionService(
        clients=bundle.clients,
        orders=bundle.orders,
        tasks=bundle.tasks,
        events=bundle.events,
        blockers=bundle.blockers,
    ).build_order_state_projection("order_001")

    assert projection.order_id == "order_001"
    assert projection.quote_ref == "quote_001"
