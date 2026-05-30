"""Order query services for Operational Registry v0.2."""

from forprint_operational_registry.dto.queries import (
    GetOrderHistoryQuery,
    GetOrderStateQuery,
    ListOrdersByClientQuery,
    ListOrdersByStatusQuery,
    ListTasksByOrderQuery,
    OrderHistorySnapshot,
    OrderStateSnapshot,
)
from forprint_operational_registry.models.order import OrderRecord
from forprint_operational_registry.models.task import OperationalTask
from forprint_operational_registry.repositories.interfaces import (
    OperationalEventRepository,
    OrderRepository,
    TaskRepository,
)


class OrderQueryService:
    """Read current operational order state."""

    def __init__(
        self,
        orders: OrderRepository,
        tasks: TaskRepository,
    ) -> None:
        self._orders = orders
        self._tasks = tasks

    def get_order_state(self, query: GetOrderStateQuery) -> OrderStateSnapshot:
        """Return current operational state snapshot."""

        order = self._orders.get(query.order_id)
        if order is None:
            raise KeyError(f"Order not found: {query.order_id}")

        return OrderStateSnapshot(
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
            updated_at=order.updated_at,
        )

    def list_orders_by_client(self, query: ListOrdersByClientQuery) -> tuple[OrderRecord, ...]:
        """List orders by client id."""

        return self._orders.list_by_client(query.client_id)

    def list_orders_by_status(self, query: ListOrdersByStatusQuery) -> tuple[OrderRecord, ...]:
        """List orders by operational status."""

        return self._orders.list_by_status(query.order_status)

    def list_tasks_by_order(self, query: ListTasksByOrderQuery) -> tuple[OperationalTask, ...]:
        """List tasks for order."""

        return self._tasks.list_by_order(query.order_id)


class OrderHistoryQueryService:
    """Read append-only operational order history."""

    def __init__(self, events: OperationalEventRepository) -> None:
        self._events = events

    def get_order_history(self, query: GetOrderHistoryQuery) -> OrderHistorySnapshot:
        """Return append-only order history snapshot."""

        events = self._events.list_by_entity("order", query.order_id)
        return OrderHistorySnapshot(order_id=query.order_id, events=events)
