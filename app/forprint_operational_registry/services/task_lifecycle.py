"""Minimal task lifecycle helpers for Operational Registry v0.1."""

from datetime import UTC, datetime

from forprint_operational_registry.models.status import ensure_allowed_task_status
from forprint_operational_registry.models.task import OperationalTask


def update_task_status(task: OperationalTask, to_status: str) -> OperationalTask:
    """Update task status after validating v0.1 task status vocabulary."""

    ensure_allowed_task_status(to_status)
    task.task_status = to_status
    task.updated_at = datetime.now(UTC)
    return task
