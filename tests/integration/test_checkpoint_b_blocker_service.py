from forprint_operational_registry.dto.commands import (
    CreateOperationalBlockerCommand,
    ResolveOperationalBlockerCommand,
)
from forprint_operational_registry.repositories.memory import InMemoryRepositoryBundle
from forprint_operational_registry.services.blocker_registry import OperationalBlockerService


def test_blocker_can_block_operational_readiness() -> None:
    repositories = InMemoryRepositoryBundle()
    service = OperationalBlockerService(repositories.blockers, repositories.events)

    blocker = service.create_blocker(
        CreateOperationalBlockerCommand(
            blocker_id="blocker_001",
            entity_type="order",
            entity_id="order_001",
            blocker_type="waiting_operator_review",
            reason="Operator review is required.",
            actor_ref="operator_001",
        )
    )

    assert blocker.blocks_operational_readiness is True
    assert service.is_entity_blocked("order", "order_001") is True


def test_blocker_resolution_appends_event() -> None:
    repositories = InMemoryRepositoryBundle()
    service = OperationalBlockerService(repositories.blockers, repositories.events)

    service.create_blocker(
        CreateOperationalBlockerCommand(
            blocker_id="blocker_001",
            entity_type="order",
            entity_id="order_001",
            blocker_type="waiting_payment_reference",
            reason="Payment reference is pending.",
            actor_ref="operator_001",
        )
    )

    resolved_blocker = service.resolve_blocker(
        ResolveOperationalBlockerCommand(
            blocker_id="blocker_001",
            actor_ref="operator_001",
            reason="Payment reference confirmed.",
        )
    )

    events = repositories.events.list_by_entity("order", "order_001")

    assert resolved_blocker.status == "resolved"
    assert service.is_entity_blocked("order", "order_001") is False
    assert events[-1].event_type == "operational_blocker_resolved"
