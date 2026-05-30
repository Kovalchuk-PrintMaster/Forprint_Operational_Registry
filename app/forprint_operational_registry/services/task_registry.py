"""Task registry service for Operational Registry v0.2."""

from datetime import UTC, datetime
from uuid import uuid4

from forprint_operational_registry.dto.commands import (
    AssignOperationalTaskCommand,
    ChangeTaskStatusCommand,
    CreateOperationalTaskCommand,
)
from forprint_operational_registry.models.event import OperationalEvent
from forprint_operational_registry.models.task import OperationalTask
from forprint_operational_registry.repositories.interfaces import (
    OperationalEventRepository,
    TaskRepository,
)
from forprint_operational_registry.services.task_lifecycle import update_task_status


class TaskRegistryService:
    """Create, assign and update operational tasks."""

    def __init__(
        self,
        tasks: TaskRepository,
        events: OperationalEventRepository,
    ) -> None:
        self._tasks = tasks
        self._events = events

    def create_task(self, command: CreateOperationalTaskCommand) -> OperationalTask:
        """Create operational task and append task_created event."""

        task = OperationalTask(
            task_id=command.task_id,
            order_id=command.order_id,
            task_type=command.task_type,
            assigned_to_ref=command.assigned_to_ref,
            metadata=command.metadata,
        )

        self._tasks.add(task)

        self._events.append(
            OperationalEvent(
                event_id=f"evt_{uuid4().hex}",
                entity_type="order",
                entity_id=task.order_id,
                event_type="task_created",
                actor_ref=command.actor_ref,
                source_module=command.source_module,
                payload={
                    "task_id": task.task_id,
                    "task_type": task.task_type,
                    "assigned_to_ref": task.assigned_to_ref,
                },
            )
        )

        return task

    def assign_task(self, command: AssignOperationalTaskCommand) -> OperationalTask:
        """Assign existing operational task and append task_assigned event."""

        task = self._tasks.get(command.task_id)
        if task is None:
            raise KeyError(f"Task not found: {command.task_id}")

        previous_assignee = task.assigned_to_ref
        task.assigned_to_ref = command.assigned_to_ref
        task.updated_at = datetime.now(UTC)
        self._tasks.save(task)

        self._events.append(
            OperationalEvent(
                event_id=f"evt_{uuid4().hex}",
                entity_type="order",
                entity_id=task.order_id,
                event_type="task_assigned",
                actor_ref=command.actor_ref,
                source_module=command.source_module,
                payload={
                    "task_id": task.task_id,
                    "previous_assignee": previous_assignee,
                    "assigned_to_ref": task.assigned_to_ref,
                },
            )
        )

        return task

    def change_task_status(self, command: ChangeTaskStatusCommand) -> OperationalTask:
        """Change operational task status and append task_status_changed event."""

        task = self._tasks.get(command.task_id)
        if task is None:
            raise KeyError(f"Task not found: {command.task_id}")

        from_status = task.task_status
        update_task_status(task, command.to_status)
        self._tasks.save(task)

        self._events.append(
            OperationalEvent(
                event_id=f"evt_{uuid4().hex}",
                entity_type="order",
                entity_id=task.order_id,
                event_type="task_status_changed",
                actor_ref=command.actor_ref,
                source_module=command.source_module,
                payload={
                    "task_id": task.task_id,
                    "from_status": from_status,
                    "to_status": task.task_status,
                },
            )
        )

        return task
