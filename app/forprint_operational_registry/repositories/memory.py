"""In-memory repository implementations for Operational Registry v0.2."""

from dataclasses import dataclass, field

from forprint_operational_registry.models.blockers import OperationalBlocker
from forprint_operational_registry.models.client import ClientRecord
from forprint_operational_registry.models.event import OperationalEvent
from forprint_operational_registry.models.note import OperationalNote
from forprint_operational_registry.models.order import OrderRecord
from forprint_operational_registry.models.task import OperationalTask


class InMemoryClientRepository:
    """In-memory client repository."""

    def __init__(self) -> None:
        self._clients: dict[str, ClientRecord] = {}

    def add(self, client: ClientRecord) -> None:
        self._clients[client.client_id] = client

    def get(self, client_id: str) -> ClientRecord | None:
        return self._clients.get(client_id)


class InMemoryOrderRepository:
    """In-memory order repository."""

    def __init__(self) -> None:
        self._orders: dict[str, OrderRecord] = {}

    def add(self, order: OrderRecord) -> None:
        self._orders[order.order_id] = order

    def save(self, order: OrderRecord) -> None:
        self._orders[order.order_id] = order

    def get(self, order_id: str) -> OrderRecord | None:
        return self._orders.get(order_id)

    def list_by_client(self, client_id: str) -> tuple[OrderRecord, ...]:
        return tuple(order for order in self._orders.values() if order.client_id == client_id)

    def list_by_status(self, order_status: str) -> tuple[OrderRecord, ...]:
        return tuple(order for order in self._orders.values() if order.order_status == order_status)


class InMemoryTaskRepository:
    """In-memory task repository."""

    def __init__(self) -> None:
        self._tasks: dict[str, OperationalTask] = {}

    def add(self, task: OperationalTask) -> None:
        self._tasks[task.task_id] = task

    def save(self, task: OperationalTask) -> None:
        self._tasks[task.task_id] = task

    def get(self, task_id: str) -> OperationalTask | None:
        return self._tasks.get(task_id)

    def list_by_order(self, order_id: str) -> tuple[OperationalTask, ...]:
        return tuple(task for task in self._tasks.values() if task.order_id == order_id)


class InMemoryOperationalEventRepository:
    """Append-only in-memory event repository."""

    def __init__(self) -> None:
        self._events: dict[tuple[str, str], list[OperationalEvent]] = {}

    def append(self, event: OperationalEvent) -> None:
        key = (event.entity_type, event.entity_id)
        self._events.setdefault(key, []).append(event)

    def list_by_entity(self, entity_type: str, entity_id: str) -> tuple[OperationalEvent, ...]:
        return tuple(self._events.get((entity_type, entity_id), []))


class InMemoryOperationalNoteRepository:
    """In-memory operational note repository."""

    def __init__(self) -> None:
        self._notes: dict[str, OperationalNote] = {}

    def add(self, note: OperationalNote) -> None:
        self._notes[note.note_id] = note

    def get(self, note_id: str) -> OperationalNote | None:
        return self._notes.get(note_id)

    def list_by_order(self, order_id: str) -> tuple[OperationalNote, ...]:
        return tuple(note for note in self._notes.values() if note.order_id == order_id)


class InMemoryOperationalBlockerRepository:
    """In-memory operational blocker repository."""

    def __init__(self) -> None:
        self._blockers: dict[str, OperationalBlocker] = {}

    def add(self, blocker: OperationalBlocker) -> None:
        self._blockers[blocker.blocker_id] = blocker

    def save(self, blocker: OperationalBlocker) -> None:
        self._blockers[blocker.blocker_id] = blocker

    def get(self, blocker_id: str) -> OperationalBlocker | None:
        return self._blockers.get(blocker_id)

    def list_by_entity(
        self,
        entity_type: str,
        entity_id: str,
    ) -> tuple[OperationalBlocker, ...]:
        return tuple(
            blocker
            for blocker in self._blockers.values()
            if blocker.entity_type == entity_type and blocker.entity_id == entity_id
        )

    def list_open_by_entity(
        self,
        entity_type: str,
        entity_id: str,
    ) -> tuple[OperationalBlocker, ...]:
        return tuple(
            blocker
            for blocker in self.list_by_entity(
                entity_type=entity_type,
                entity_id=entity_id,
            )
            if blocker.status == "open"
        )


@dataclass(slots=True)
class InMemoryRepositoryBundle:
    """Convenience bundle for tests and local v0.2/v0.3 development."""

    clients: InMemoryClientRepository = field(default_factory=InMemoryClientRepository)
    orders: InMemoryOrderRepository = field(default_factory=InMemoryOrderRepository)
    tasks: InMemoryTaskRepository = field(default_factory=InMemoryTaskRepository)
    events: InMemoryOperationalEventRepository = field(
        default_factory=InMemoryOperationalEventRepository
    )
    notes: InMemoryOperationalNoteRepository = field(
        default_factory=InMemoryOperationalNoteRepository
    )
    blockers: InMemoryOperationalBlockerRepository = field(
        default_factory=InMemoryOperationalBlockerRepository
    )


notes: InMemoryOperationalNoteRepository = field(default_factory=InMemoryOperationalNoteRepository)
