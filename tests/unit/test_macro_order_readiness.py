from forprint_operational_registry.dto.commands import (
    CreateOperationalBlockerCommand,
    CreateOrderCommand,
    ResolveOperationalBlockerCommand,
)
from forprint_operational_registry.repositories.memory import InMemoryRepositoryBundle
from forprint_operational_registry.services.blocker_registry import OperationalBlockerService
from forprint_operational_registry.services.order_readiness import OrderReadinessService
from forprint_operational_registry.services.order_registry import OrderRegistryService


def test_readiness_is_blocked_by_active_blocker() -> None:
    repositories = InMemoryRepositoryBundle()
    OrderRegistryService(repositories.orders, repositories.events).create_order(
        CreateOrderCommand(
            order_id="order_001",
            client_id="client_001",
            source_channel="crm_manual",
            quote_ref="quote_001",
        )
    )
    OperationalBlockerService(repositories.blockers, repositories.events).create_blocker(
        CreateOperationalBlockerCommand(
            blocker_id="blocker_001",
            entity_type="order",
            entity_id="order_001",
            blocker_type="manual_review_required",
            reason="Manual review required.",
        )
    )

    snapshot = OrderReadinessService(
        repositories.orders,
        repositories.blockers,
    ).build_readiness_snapshot("order_001")

    assert snapshot.readiness_status == "blocked"
    assert snapshot.is_ready_for_next_stage is False


def test_readiness_improves_after_blocker_resolved() -> None:
    repositories = InMemoryRepositoryBundle()
    OrderRegistryService(repositories.orders, repositories.events).create_order(
        CreateOrderCommand(
            order_id="order_001",
            client_id="client_001",
            source_channel="crm_manual",
            quote_ref="quote_001",
        )
    )
    blocker_service = OperationalBlockerService(repositories.blockers, repositories.events)
    blocker_service.create_blocker(
        CreateOperationalBlockerCommand(
            blocker_id="blocker_001",
            entity_type="order",
            entity_id="order_001",
            blocker_type="manual_review_required",
            reason="Manual review required.",
        )
    )
    blocker_service.resolve_blocker(
        ResolveOperationalBlockerCommand(
            blocker_id="blocker_001",
            actor_ref="operator_001",
        )
    )

    snapshot = OrderReadinessService(
        repositories.orders,
        repositories.blockers,
    ).build_readiness_snapshot("order_001")

    assert snapshot.readiness_status == "ready"
    assert snapshot.is_ready_for_next_stage is True


def test_missing_calculation_reference_creates_readiness_warning() -> None:
    repositories = InMemoryRepositoryBundle()
    OrderRegistryService(repositories.orders, repositories.events).create_order(
        CreateOrderCommand(
            order_id="order_001",
            client_id="client_001",
            source_channel="crm_manual",
        )
    )

    snapshot = OrderReadinessService(
        repositories.orders,
        repositories.blockers,
    ).build_readiness_snapshot("order_001")

    assert snapshot.readiness_status == "warning"
    assert "missing_calculation" in snapshot.missing_references


def test_payment_reference_pending_blocks_production_readiness() -> None:
    repositories = InMemoryRepositoryBundle()
    service = OrderRegistryService(repositories.orders, repositories.events)
    order = service.create_order(
        CreateOrderCommand(
            order_id="order_001",
            client_id="client_001",
            source_channel="crm_manual",
            quote_ref="quote_001",
        )
    )
    order.order_status = "payment_reference_pending"
    repositories.orders.save(order)

    snapshot = OrderReadinessService(
        repositories.orders,
        repositories.blockers,
    ).build_readiness_snapshot("order_001")

    assert snapshot.readiness_status == "waiting"
    assert "waiting_payment_reference" in snapshot.waiting_reasons


def test_readiness_does_not_calculate_foreign_truth() -> None:
    repositories = InMemoryRepositoryBundle()
    OrderRegistryService(repositories.orders, repositories.events).create_order(
        CreateOrderCommand(
            order_id="order_001",
            client_id="client_001",
            source_channel="crm_manual",
            quote_ref="quote_001",
        )
    )

    snapshot = OrderReadinessService(
        repositories.orders,
        repositories.blockers,
    ).build_readiness_snapshot("order_001")

    joined_notes = " ".join(snapshot.boundary_notes)

    assert "No payment balance" in joined_notes
    assert "warehouse stock" in joined_notes
    assert "calculator" in joined_notes.lower()
    assert "prepress" in joined_notes.lower()
