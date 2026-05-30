"""Internal future-facing result DTOs for Operational Registry v0.4.

These results are not HTTP responses and not Gateway envelopes.
Gateway may later wrap them.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any

from forprint_operational_registry.dto.errors import OperationalError, OperationalWarning


class OperationalResultStatus(StrEnum):
    """Allowed operational result statuses."""

    ACCEPTED = "accepted"
    APPLIED = "applied"
    REJECTED = "rejected"
    BLOCKED = "blocked"
    NOT_FOUND = "not_found"
    VALIDATION_FAILED = "validation_failed"
    CONFLICT = "conflict"
    NOOP = "noop"


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""

    return datetime.now(UTC)


def freeze_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    """Freeze mapping value."""

    return MappingProxyType(dict(value))


@dataclass(frozen=True, slots=True)
class OperationalCommandResult:
    """Internal command result.

    This is adapter-facing, not a production API response.
    """

    result_id: str
    command_id: str
    correlation_id: str
    idempotency_key: str
    status: str
    entity_type: str
    entity_id: str
    state_snapshot: Mapping[str, Any] | None = None
    events_appended: tuple[str, ...] = ()
    warnings: tuple[OperationalWarning, ...] = ()
    errors: tuple[OperationalError, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if self.state_snapshot is not None:
            object.__setattr__(self, "state_snapshot", freeze_mapping(self.state_snapshot))
        object.__setattr__(self, "metadata", freeze_mapping(self.metadata))


@dataclass(frozen=True, slots=True)
class OperationalQueryResult:
    """Internal query result."""

    result_id: str
    correlation_id: str
    status: str
    result_type: str
    payload: Mapping[str, Any]
    warnings: tuple[OperationalWarning, ...] = ()
    errors: tuple[OperationalError, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        object.__setattr__(self, "payload", freeze_mapping(self.payload))
        object.__setattr__(self, "metadata", freeze_mapping(self.metadata))
