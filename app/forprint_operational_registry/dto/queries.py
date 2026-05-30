"""Internal query DTOs and snapshots for Operational Registry v0.2."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from forprint_operational_registry.models.event import OperationalEvent


@dataclass(frozen=True, slots=True)
class GetOrderByIdQuery:
    """Read order by id."""

    order_id: str


@dataclass(frozen=True, slots=True)
class ListOrdersByClientQuery:
    """List operational orders for client."""

    client_id: str


@dataclass(frozen=True, slots=True)
class ListTasksByOrderQuery:
    """List operational tasks for order."""

    order_id: str


@dataclass(frozen=True, slots=True)
class GetOrderStateQuery:
    """Read current operational order state."""

    order_id: str


@dataclass(frozen=True, slots=True)
class GetOrderHistoryQuery:
    """Read append-only operational order history."""

    order_id: str


@dataclass(frozen=True, slots=True)
class ListOrdersByStatusQuery:
    """List orders by operational status."""

    order_status: str


@dataclass(frozen=True, slots=True)
class OrderStateSnapshot:
    """Operational state snapshot returned by query service.

    This is not a CRM dashboard and not an accounting projection.
    """

    order_id: str
    client_id: str
    order_status: str
    workflow_status: str
    source_channel: str
    quote_ref: str | None
    accounting_refs: Mapping[str, Any] = field(default_factory=dict)
    production_refs: Mapping[str, Any] = field(default_factory=dict)
    prepress_refs: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class OrderHistorySnapshot:
    """Append-only operational order history snapshot."""

    order_id: str
    events: tuple[OperationalEvent, ...]
