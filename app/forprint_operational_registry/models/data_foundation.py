"""ForPrint operational data foundation base concepts.

These are lightweight policy/domain concepts for future modeling.
They are not real product/material/supplier catalogs and not production integrations.
"""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""

    return datetime.now(UTC)


def freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    """Freeze mapping to avoid accidental mutation."""

    return MappingProxyType(dict(value or {}))


def freeze_tuple(value: Sequence[str] | None) -> tuple[str, ...]:
    """Freeze sequence as tuple."""

    return tuple(value or ())


def freeze_rows(value: Sequence[Mapping[str, Any]] | None) -> tuple[Mapping[str, Any], ...]:
    """Freeze projection rows."""

    return tuple(freeze_mapping(row) for row in value or ())


@dataclass(frozen=True, slots=True)
class RawNormalizedValue:
    """Raw + normalized value pair for imported data."""

    raw_value: str
    normalized_value: str | None = None
    source_system: str = "unknown"
    source_ref: str | None = None

    def __post_init__(self) -> None:
        if not self.raw_value:
            raise ValueError("raw_value is required")

        if not self.source_system:
            raise ValueError("source_system is required")


@dataclass(frozen=True, slots=True)
class MasterDataRecord:
    """Base concept for stable reference entities.

    internal_id is logic truth.
    display_name is user-facing and editable.
    raw_source_name preserves imported historical value.
    """

    internal_id: str
    entity_type: str
    display_name: str
    canonical_name: str | None = None
    status: str = "active"
    source_system: str = "manual"
    raw_source_name: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.internal_id:
            raise ValueError("internal_id is required")

        if not self.entity_type:
            raise ValueError("entity_type is required")

        if not self.display_name:
            raise ValueError("display_name is required")

        object.__setattr__(self, "metadata", freeze_mapping(self.metadata))


@dataclass(frozen=True, slots=True)
class OperationalFactRecord:
    """Base concept for transactional/operational facts."""

    fact_id: str
    fact_type: str
    business_date: datetime
    client_account_id: str | None = None
    source_system: str = "manual"
    source_ref: str | None = None
    status: str = "active"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    raw_values: Mapping[str, RawNormalizedValue] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.fact_id:
            raise ValueError("fact_id is required")

        if not self.fact_type:
            raise ValueError("fact_type is required")

        if not self.source_system:
            raise ValueError("source_system is required")

        object.__setattr__(self, "raw_values", freeze_mapping(self.raw_values))
        object.__setattr__(self, "metadata", freeze_mapping(self.metadata))


@dataclass(frozen=True, slots=True)
class OperationalEventRecord:
    """Append-only event concept for operational history."""

    event_id: str
    event_type: str
    target_entity_type: str
    target_entity_id: str
    occurred_at: datetime = field(default_factory=utc_now)
    actor_ref: str | None = None
    source_system: str = "manual"
    payload: Mapping[str, Any] = field(default_factory=dict)
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.event_id:
            raise ValueError("event_id is required")

        if not self.event_type:
            raise ValueError("event_type is required")

        if not self.target_entity_type:
            raise ValueError("target_entity_type is required")

        if not self.target_entity_id:
            raise ValueError("target_entity_id is required")

        object.__setattr__(self, "payload", freeze_mapping(self.payload))


@dataclass(frozen=True, slots=True)
class ExternalReference:
    """Generic reference to external systems.

    External codes/refs are not ForPrint primary IDs.
    """

    external_reference_id: str
    internal_entity_type: str
    internal_entity_id: str
    external_system: str
    external_entity_type: str
    external_code: str | None = None
    external_ref: str | None = None
    external_name: str | None = None
    raw_payload: Mapping[str, Any] = field(default_factory=dict)
    sync_status: str = "seen"
    last_seen_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.external_reference_id:
            raise ValueError("external_reference_id is required")

        if not self.internal_entity_type:
            raise ValueError("internal_entity_type is required")

        if not self.internal_entity_id:
            raise ValueError("internal_entity_id is required")

        if not self.external_system:
            raise ValueError("external_system is required")

        if not self.external_entity_type:
            raise ValueError("external_entity_type is required")

        object.__setattr__(self, "raw_payload", freeze_mapping(self.raw_payload))


@dataclass(frozen=True, slots=True)
class DataProjection:
    """Base concept for reporting output."""

    projection_id: str
    projection_type: str
    generated_at: datetime = field(default_factory=utc_now)
    period_start: datetime | None = None
    period_end: datetime | None = None
    dimensions: tuple[str, ...] = ()
    metrics: tuple[str, ...] = ()
    rows: tuple[Mapping[str, Any], ...] = ()
    source_refs: Mapping[str, Any] = field(default_factory=dict)
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.projection_id:
            raise ValueError("projection_id is required")

        if not self.projection_type:
            raise ValueError("projection_type is required")

        object.__setattr__(self, "dimensions", freeze_tuple(self.dimensions))
        object.__setattr__(self, "metrics", freeze_tuple(self.metrics))
        object.__setattr__(self, "rows", freeze_rows(self.rows))
        object.__setattr__(self, "source_refs", freeze_mapping(self.source_refs))
        object.__setattr__(self, "warnings", freeze_tuple(self.warnings))


@dataclass(frozen=True, slots=True)
class ReportDefinition:
    """Configurable report definition concept."""

    report_definition_id: str
    report_name: str
    report_type: str
    description: str | None = None
    dimensions: tuple[str, ...] = ()
    metrics: tuple[str, ...] = ()
    filters: Mapping[str, Any] = field(default_factory=dict)
    default_period: str | None = None
    status: str = "draft"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.report_definition_id:
            raise ValueError("report_definition_id is required")

        if not self.report_name:
            raise ValueError("report_name is required")

        if not self.report_type:
            raise ValueError("report_type is required")

        object.__setattr__(self, "dimensions", freeze_tuple(self.dimensions))
        object.__setattr__(self, "metrics", freeze_tuple(self.metrics))
        object.__setattr__(self, "filters", freeze_mapping(self.filters))
