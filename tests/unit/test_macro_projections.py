from forprint_operational_registry.dto.commands import (
    CreateClientCommand,
    CreateOperationalBlockerCommand,
    CreateOperationalTaskCommand,
    CreateOrderCommand,
)
from forprint_operational_registry.repositories.memory import InMemoryRepositoryBundle
from forprint_operational_registry.services.blocker_registry import OperationalBlockerService
from forprint_operational_registry.services.client_registry import ClientRegistryService
from forprint_operational_registry.services.order_registry import OrderRegistryService
from forprint_operational_registry.services.projections import OperationalProjectionService
from forprint_operational_registry.services.task_registry import TaskRegistryService


def build_projection_service() -> tuple[InMemoryRepositoryBundle, OperationalProjectionService]:
    repositories = InMemoryRepositoryBundle()
    ClientRegistryService(repositories.clients).create_client(
        CreateClientCommand(client_id="client_001", display_name="Test Client")
    )
    OrderRegistryService(repositories.orders, repositories.events).create_order(
        CreateOrderCommand(
            order_id="order_001",
            client_id="client_001",
            source_channel="crm_manual",
            quote_ref="quote_001",
            accounting_refs={"accounting_invoice_ref": "invoice_001"},
            prepress_refs={"prepress_job_ref": "prepress_001"},
        )
    )
    TaskRegistryService(repositories.tasks, repositories.events).create_task(
        CreateOperationalTaskCommand(
            task_id="task_001",
            order_id="order_001",
            task_type="prepress_review",
        )
    )
    service = OperationalProjectionService(
        clients=repositories.clients,
        orders=repositories.orders,
        tasks=repositories.tasks,
        events=repositories.events,
        blockers=repositories.blockers,
    )
    return repositories, service


def test_order_state_projection_can_be_generated() -> None:
    _, service = build_projection_service()

    projection = service.build_order_state_projection("order_001")

    assert projection.order_id == "order_001"
    assert projection.quote_ref == "quote_001"
    assert "accounting_invoice_ref" in projection.accounting_refs
    assert "prepress_job_ref" in projection.prepress_refs


def test_order_list_item_projection_can_be_generated() -> None:
    _, service = build_projection_service()

    projection = service.build_order_list_item_projection("order_001")

    assert projection.order_id == "order_001"
    assert projection.is_blocked is False


def test_task_board_projection_can_be_generated() -> None:
    _, service = build_projection_service()

    projection = service.build_task_board_projection("order_001")

    assert projection.order_id == "order_001"
    assert len(projection.tasks) == 1
    assert "new" in projection.tasks_by_status


def test_operational_timeline_projection_uses_append_only_events() -> None:
    _, service = build_projection_service()

    timeline = service.build_operational_timeline_projection("order", "order_001")

    assert timeline.entity_type == "order"
    assert timeline.events[0].event_type == "order_created"


def test_readiness_reflects_active_blockers() -> None:
    repositories, service = build_projection_service()
    OperationalBlockerService(repositories.blockers, repositories.events).create_blocker(
        CreateOperationalBlockerCommand(
            blocker_id="blocker_001",
            entity_type="order",
            entity_id="order_001",
            blocker_type="waiting_operator_review",
            reason="Operator review required.",
        )
    )

    projection = service.build_order_state_projection("order_001")

    assert projection.is_blocked is True
    assert projection.active_blockers_count == 1
    assert projection.readiness_status == "blocked"


def test_projection_does_not_include_foreign_owned_objects() -> None:
    _, service = build_projection_service()

    projection = service.build_order_state_projection("order_001")

    assert not hasattr(projection, "invoice")
    assert not hasattr(projection, "payment")
    assert not hasattr(projection, "product_catalog")
    assert not hasattr(projection, "material_catalog")
