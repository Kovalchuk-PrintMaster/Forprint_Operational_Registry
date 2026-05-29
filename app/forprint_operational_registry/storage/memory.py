"""In-memory storage foundation for Operational Registry v0.1."""

from forprint_operational_registry.models.client import ClientRecord
from forprint_operational_registry.models.event import OperationalEvent
from forprint_operational_registry.models.order import OrderRecord
from forprint_operational_registry.models.task import OperationalTask


class InMemoryOperationalRegistry:
    """Small in-memory repository for tests and bootstrap development."""

    def __init__(self) -> None:
        self.clients: dict[str, ClientRecord] = {}
        self.orders: dict[str, OrderRecord] = {}
        self.tasks: dict[str, OperationalTask] = {}
        self._order_events: dict[str, list[OperationalEvent]] = {}

    def add_client(self, client: ClientRecord) -> None:
        self.clients[client.client_id] = client

    def add_order(self, order: OrderRecord) -> None:
        self.orders[order.order_id] = order
        self._order_events.setdefault(order.order_id, [])

    def add_task(self, task: OperationalTask) -> None:
        self.tasks[task.task_id] = task

    def get_order(self, order_id: str) -> OrderRecord:
        return self.orders[order_id]

    def append_order_event(self, event: OperationalEvent) -> None:
        if event.entity_type != "order":
            raise ValueError("Only order events are supported by this v0.1 helper")

        self._order_events.setdefault(event.entity_id, []).append(event)

    def list_order_events(self, order_id: str) -> tuple[OperationalEvent, ...]:
        return tuple(self._order_events.get(order_id, []))
