"""Order readiness service for Operational Registry v0.3."""

from forprint_operational_registry.dto.projections import OperationalReadinessSnapshot
from forprint_operational_registry.repositories.interfaces import (
    OperationalBlockerRepository,
    OrderRepository,
)


class OrderReadinessService:
    """Evaluate internal operational readiness without calling foreign modules."""

    def __init__(
        self,
        orders: OrderRepository,
        blockers: OperationalBlockerRepository,
    ) -> None:
        self._orders = orders
        self._blockers = blockers

    def build_readiness_snapshot(self, order_id: str) -> OperationalReadinessSnapshot:
        """Build operational readiness snapshot for order."""

        order = self._orders.get(order_id)
        if order is None:
            raise KeyError(f"Order not found: {order_id}")

        active_blockers = self._blockers.list_open_by_entity("order", order_id)
        active_blocker_ids = tuple(blocker.blocker_id for blocker in active_blockers)

        missing_references: list[str] = []
        waiting_reasons: list[str] = []

        if not order.quote_ref and not order.metadata.get("calculator_result_ref"):
            missing_references.append("missing_calculation")

        if order.order_status == "payment_reference_pending":
            waiting_reasons.append("waiting_payment_reference")

        if active_blockers:
            readiness_status = "blocked"
        elif waiting_reasons:
            readiness_status = "waiting"
        elif missing_references:
            readiness_status = "warning"
        else:
            readiness_status = "ready"

        return OperationalReadinessSnapshot(
            order_id=order.order_id,
            readiness_status=readiness_status,
            is_ready_for_next_stage=readiness_status == "ready",
            active_blocker_ids=active_blocker_ids,
            missing_references=tuple(missing_references),
            waiting_reasons=tuple(waiting_reasons),
            boundary_notes=(
                "Readiness uses operational state and references only.",
                "No payment balance, warehouse stockCalculator or prepress execution is performed.",
            ),
        )
