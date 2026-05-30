"""Operational projection services for v0.3."""

from collections import defaultdict

from forprint_operational_registry.dto.projections import (
    ClientOperationalSummary,
    OperationalHealthSnapshot,
    OperationalTimelineProjection,
    OrderListItemProjection,
    OrderStateProjection,
    TaskBoardProjection,
)
from forprint_operational_registry.repositories.interfaces import (
    ClientRepository,
    OperationalBlockerRepository,
    OperationalEventRepository,
    OrderRepository,
    TaskRepository,
)


class OperationalProjectionService:
    """Build stable read-side operational projections."""

    def __init__(
        self,
        clients: ClientRepository,
        orders: OrderRepository,
        tasks: TaskRepository,
        events: OperationalEventRepository,
        blockers: OperationalBlockerRepository,
    ) -> None:
        self._clients = clients
        self._orders = orders
        self._tasks = tasks
        self._events = events
        self._blockers = blockers

    def build_order_state_projection(self, order_id: str) -> OrderStateProjection:
        """Build current order state projection."""

        order = self._orders.get(order_id)
        if order is None:
            raise KeyError(f"Order not found: {order_id}")

        active_blockers = self._blockers.list_open_by_entity("order", order_id)

        readiness_status = "blocked" if active_blockers else "available"

        if order.order_status == "payment_reference_pending":
            readiness_status = "waiting_payment_reference"

        if order.order_status in {"completed", "cancelled"}:
            readiness_status = "terminal"

        return OrderStateProjection(
            order_id=order.order_id,
            client_id=order.client_id,
            order_status=order.order_status,
            workflow_status=order.workflow_status,
            source_channel=order.source_channel,
            quote_ref=order.quote_ref,
            accounting_refs=order.accounting_refs,
            production_refs=order.production_refs,
            prepress_refs=order.prepress_refs,
            metadata=order.metadata,
            active_blockers_count=len(active_blockers),
            is_blocked=bool(active_blockers),
            readiness_status=readiness_status,
            updated_at=order.updated_at,
        )

    def build_order_list_item_projection(self, order_id: str) -> OrderListItemProjection:
        """Build compact order list item projection."""

        order = self._orders.get(order_id)
        if order is None:
            raise KeyError(f"Order not found: {order_id}")

        active_blockers = self._blockers.list_open_by_entity("order", order_id)

        return OrderListItemProjection(
            order_id=order.order_id,
            client_id=order.client_id,
            order_status=order.order_status,
            source_channel=order.source_channel,
            is_blocked=bool(active_blockers),
            active_blockers_count=len(active_blockers),
            updated_at=order.updated_at,
        )

    def build_client_operational_summary(self, client_id: str) -> ClientOperationalSummary:
        """Build client operational summary."""

        if self._clients.get(client_id) is None:
            raise KeyError(f"Client not found: {client_id}")

        orders = self._orders.list_by_client(client_id)
        active_statuses = {
            "new",
            "needs_review",
            "quote_pending",
            "quote_accepted",
            "payment_reference_pending",
            "payment_reference_confirmed",
            "in_prepress",
            "ready_for_production",
            "in_production",
            "ready_for_pickup",
            "blocked",
        }

        blocked_orders_count = sum(
            1 for order in orders if self._blockers.list_open_by_entity("order", order.order_id)
        )

        return ClientOperationalSummary(
            client_id=client_id,
            orders_count=len(orders),
            active_orders_count=sum(1 for order in orders if order.order_status in active_statuses),
            blocked_orders_count=blocked_orders_count,
            completed_orders_count=sum(1 for order in orders if order.order_status == "completed"),
        )

    def build_task_board_projection(self, order_id: str) -> TaskBoardProjection:
        """Build task board projection for order."""

        tasks = self._tasks.list_by_order(order_id)
        tasks_by_status: dict[str, list] = defaultdict(list)

        for task in tasks:
            tasks_by_status[task.task_status].append(task)

        return TaskBoardProjection(
            order_id=order_id,
            tasks=tasks,
            tasks_by_status={
                status: tuple(status_tasks) for status, status_tasks in tasks_by_status.items()
            },
        )

    def build_operational_timeline_projection(
        self,
        entity_type: str,
        entity_id: str,
    ) -> OperationalTimelineProjection:
        """Build append-only timeline projection."""

        return OperationalTimelineProjection(
            entity_type=entity_type,
            entity_id=entity_id,
            events=self._events.list_by_entity(entity_type, entity_id),
        )

    def build_health_snapshot(self) -> OperationalHealthSnapshot:
        """Build local module health snapshot."""

        return OperationalHealthSnapshot(
            module_id="forprint_operational_registry",
            module_status="v0.3_internal_readiness",
            implemented_layers=(
                "domain_models",
                "command_query_dtos",
                "repository_interfaces",
                "in_memory_repositories",
                "service_layer",
                "lifecycle_validation",
                "operational_blockers",
                "operational_projections",
                "handoff_fixtures",
            ),
            open_questions=(
                "v0.4 production API decision",
                "v0.4 storage strategy decision",
                "future Gateway/CRM adapter contracts",
            ),
        )
