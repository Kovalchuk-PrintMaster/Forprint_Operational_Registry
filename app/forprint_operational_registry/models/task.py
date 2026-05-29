"""Operational task model."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from forprint_operational_registry.models.status import ensure_allowed_task_status


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""

    return datetime.now(UTC)


@dataclass(slots=True)
class OperationalTask:
    """Operational task attached to an order or workflow."""

    task_id: str
    order_id: str
    task_type: str
    task_status: str = "new"
    assigned_to_ref: str | None = None
    deadline: datetime | None = None
    blocking_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.task_id:
            raise ValueError("task_id is required")

        if not self.order_id:
            raise ValueError("order_id is required")

        if not self.task_type:
            raise ValueError("task_type is required")

        ensure_allowed_task_status(self.task_status)
