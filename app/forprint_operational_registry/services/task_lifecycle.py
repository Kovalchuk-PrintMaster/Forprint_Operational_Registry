"""Task lifecycle helpers for Operational Registry v0.3."""

from datetime import UTC, datetime

from forprint_operational_registry.models.status import ensure_allowed_task_status
from forprint_operational_registry.models.task import OperationalTask


class InvalidTaskTransition(ValueError):
    """Raised when task status transition is not allowed."""


GENERIC_TASK_LIFECYCLE_V0: dict[str, set[str]] = {
    "new": {"assigned", "in_progress", "blocked", "cancelled"},
    "assigned": {"in_progress", "blocked", "completed", "cancelled"},
    "in_progress": {"blocked", "completed", "cancelled"},
    "blocked": {"assigned", "in_progress", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}

TERMINAL_TASK_STATUSES: tuple[str, ...] = ("completed", "cancelled")


def validate_task_transition(from_status: str, to_status: str) -> None:
    """Validate generic v0 task transition."""

    ensure_allowed_task_status(from_status)
    ensure_allowed_task_status(to_status)

    if from_status == to_status:
        raise InvalidTaskTransition(f"Task is already in status: {to_status}")

    if from_status in TERMINAL_TASK_STATUSES:
        raise InvalidTaskTransition(f"Cannot transition from terminal task status: {from_status}")

    if to_status not in GENERIC_TASK_LIFECYCLE_V0[from_status]:
        raise InvalidTaskTransition(f"Invalid task transition: {from_status} -> {to_status}")


def update_task_status(task: OperationalTask, to_status: str) -> OperationalTask:
    """Update task status after validating v0.3 task lifecycle."""

    validate_task_transition(task.task_status, to_status)
    task.task_status = to_status
    task.updated_at = datetime.now(UTC)
    return task
