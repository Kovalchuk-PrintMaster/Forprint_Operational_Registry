import pytest
from forprint_operational_registry.models.blockers import OperationalBlocker


def test_operational_blocker_can_be_created() -> None:
    blocker = OperationalBlocker(
        blocker_id="blocker_001",
        entity_type="order",
        entity_id="order_001",
        blocker_type="waiting_prepress_check",
        reason="Prepress check is not finished.",
        source_module="forprint_operational_registry",
    )

    assert blocker.blocker_id == "blocker_001"
    assert blocker.blocks_operational_readiness is True


def test_operational_blocker_can_be_resolved() -> None:
    blocker = OperationalBlocker(
        blocker_id="blocker_001",
        entity_type="order",
        entity_id="order_001",
        blocker_type="manual_review_required",
        reason="Operator must review order.",
        source_module="forprint_operational_registry",
    )

    blocker.resolve()

    assert blocker.status == "resolved"
    assert blocker.blocks_operational_readiness is False
    assert blocker.resolved_at is not None


def test_blocker_does_not_become_foreign_domain_truth() -> None:
    with pytest.raises(ValueError, match="must not become foreign-domain truth"):
        OperationalBlocker(
            blocker_id="blocker_001",
            entity_type="order",
            entity_id="order_001",
            blocker_type="waiting_payment_reference",
            reason="Payment reference is missing.",
            source_module="forprint_operational_registry",
            metadata={"payment_truth": "paid"},
        )
