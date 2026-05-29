"""Append-only operational event model."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""

    return datetime.now(UTC)


def freeze_payload(value: Any) -> Any:
    """Recursively freeze dictionaries/lists for append-only event payloads."""

    if isinstance(value, dict):
        return MappingProxyType({key: freeze_payload(item) for key, item in value.items()})

    if isinstance(value, list):
        return tuple(freeze_payload(item) for item in value)

    return value


@dataclass(frozen=True, slots=True)
class OperationalEvent:
    """Immutable operational history event.

    Existing events are not edited in place.
    State changes should append new events.
    """

    event_id: str
    entity_type: str
    entity_id: str
    event_type: str
    actor_ref: str
    source_module: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.event_id:
            raise ValueError("event_id is required")

        if not self.entity_type:
            raise ValueError("entity_type is required")

        if not self.entity_id:
            raise ValueError("entity_id is required")

        if not self.event_type:
            raise ValueError("event_type is required")

        object.__setattr__(self, "payload", freeze_payload(dict(self.payload)))
