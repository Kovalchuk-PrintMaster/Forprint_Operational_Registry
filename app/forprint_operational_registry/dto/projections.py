"""Read-side operational projections for Operational Registry v0.3."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from forprint_operational_registry.models.event import OperationalEvent
from forprint_operational_registry.models.task import OperationalTask


@dataclass(frozen=True, slots=True)
class OrderStateProjection:
    """Stable operational order state projection.

    This is not CRM dashboard layout and not accounting truth.
    """

    order_id: str
    client_id: str
    order_status: str
    workflow_status: str
    source_channel: str
    quote_ref: str | None = None
    accounting_refs: Mapping[str, Any] = field(default_factory=dict)
    production_refs: Mapping[str, Any] = field(default_factory=dict)
    prepress_refs: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)
    active_blockers_count: int = 0
    is_blocked: bool = False
    readiness_status: str = "unknown"
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class OrderListItemProjection:
    """Compact order list item projection."""

    order_id: str
    client_id: str
    order_status: str
    source_channel: str
    is_blocked: bool
    active_blockers_count: int
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class ClientOperationalSummary:
    """Operational summary for client orders."""

    client_id: str
    orders_count: int
    active_orders_count: int
    blocked_orders_count: int
    completed_orders_count: int


@dataclass(frozen=True, slots=True)
class TaskBoardProjection:
    """Operational task board projection for an order."""

    order_id: str
    tasks: tuple[OperationalTask, ...]
    tasks_by_status: Mapping[str, tuple[OperationalTask, ...]]


@dataclass(frozen=True, slots=True)
class OperationalTimelineProjection:
    """Append-only operational timeline projection."""

    entity_type: str
    entity_id: str
    events: tuple[OperationalEvent, ...]


@dataclass(frozen=True, slots=True)
class OperationalReadinessSnapshot:
    """Operational readiness snapshot.

    This does not calculate payment, warehouse stock or prepress truth.
    """

    order_id: str
    readiness_status: str
    is_ready_for_next_stage: bool
    active_blocker_ids: tuple[str, ...] = ()
    missing_references: tuple[str, ...] = ()
    waiting_reasons: tuple[str, ...] = ()
    boundary_notes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class OperationalHealthSnapshot:
    """Local operational health snapshot for reporting readiness."""

    module_id: str
    module_status: str
    implemented_layers: tuple[str, ...]
    open_questions: tuple[str, ...] = ()
