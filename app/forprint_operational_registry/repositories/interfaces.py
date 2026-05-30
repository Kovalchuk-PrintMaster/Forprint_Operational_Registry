"""Storage-agnostic repository interfaces for Operational Registry v0.2."""

from typing import Protocol

from forprint_operational_registry.models.client import ClientRecord
from forprint_operational_registry.models.event import OperationalEvent
from forprint_operational_registry.models.note import OperationalNote
from forprint_operational_registry.models.order import OrderRecord
from forprint_operational_registry.models.task import OperationalTask


class ClientRepository(Protocol):
    """Repository interface for operational client identity."""

    def add(self, client: ClientRecord) -> None: ...

    def get(self, client_id: str) -> ClientRecord | None: ...


class OrderRepository(Protocol):
    """Repository interface for operational orders."""

    def add(self, order: OrderRecord) -> None: ...

    def save(self, order: OrderRecord) -> None: ...

    def get(self, order_id: str) -> OrderRecord | None: ...

    def list_by_client(self, client_id: str) -> tuple[OrderRecord, ...]: ...

    def list_by_status(self, order_status: str) -> tuple[OrderRecord, ...]: ...


class TaskRepository(Protocol):
    """Repository interface for operational tasks."""

    def add(self, task: OperationalTask) -> None: ...

    def save(self, task: OperationalTask) -> None: ...

    def get(self, task_id: str) -> OperationalTask | None: ...

    def list_by_order(self, order_id: str) -> tuple[OperationalTask, ...]: ...


class OperationalEventRepository(Protocol):
    """Append-only event repository interface."""

    def append(self, event: OperationalEvent) -> None: ...

    def list_by_entity(self, entity_type: str, entity_id: str) -> tuple[OperationalEvent, ...]: ...


class OperationalNoteRepository(Protocol):
    """Repository interface for lightweight operational notes."""

    def add(self, note: OperationalNote) -> None: ...

    def get(self, note_id: str) -> OperationalNote | None: ...

    def list_by_order(self, order_id: str) -> tuple[OperationalNote, ...]: ...
