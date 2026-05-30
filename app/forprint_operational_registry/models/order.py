"""Order model for canonical operational order state."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from forprint_operational_registry.models.status import ensure_allowed_order_status


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""

    return datetime.now(UTC)


@dataclass(slots=True)
class OrderRecord:
    """Canonical operational order state.

    The model may store references to Accounting, Calculator, Library and Prepress,
    but it must not own their canonical truth.
    """

    order_id: str
    client_id: str
    order_status: str = "new"
    workflow_status: str = "new"
    source_channel: str = "crm_manual"
    source_refs: dict[str, Any] = field(default_factory=dict)
    quote_ref: str | None = None
    accounting_refs: dict[str, Any] = field(default_factory=dict)
    production_refs: dict[str, Any] = field(default_factory=dict)
    prepress_refs: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.order_id:
            raise ValueError("order_id is required")

        if not self.client_id:
            raise ValueError("client_id is required")

        ensure_allowed_order_status(self.order_status)
        ensure_allowed_order_status(self.workflow_status)

        if not isinstance(self.source_channel, str) or not self.source_channel:
            raise ValueError("source_channel must be a flexible non-empty string")
