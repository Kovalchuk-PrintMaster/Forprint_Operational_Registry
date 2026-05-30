"""Operational note model.

Operational notes are lightweight internal annotations.
They are not CRM communication history and not accounting comments as financial truth.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

FORBIDDEN_NOTE_METADATA_KEYS: tuple[str, ...] = (
    "full_crm_interaction_history",
    "customer_chat_archive",
    "marketing_profile",
    "payment_truth",
    "invoice_truth",
)


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""

    return datetime.now(UTC)


def freeze_mapping(value: dict[str, Any]) -> Mapping[str, Any]:
    """Freeze note metadata to avoid accidental in-place mutation."""

    return MappingProxyType(dict(value))


@dataclass(frozen=True, slots=True)
class OperationalNote:
    """Lightweight operational annotation for order or task."""

    note_id: str
    order_id: str
    author_ref: str
    note_text: str
    task_id: str | None = None
    visibility: str = "internal"
    metadata: Mapping[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.note_id:
            raise ValueError("note_id is required")

        if not self.order_id:
            raise ValueError("order_id is required")

        if not self.author_ref:
            raise ValueError("author_ref is required")

        if not self.note_text:
            raise ValueError("note_text is required")

        forbidden_keys = set(self.metadata).intersection(FORBIDDEN_NOTE_METADATA_KEYS)
        if forbidden_keys:
            raise ValueError(
                "OperationalNote must not become CRM/accounting history. "
                f"Forbidden metadata keys: {sorted(forbidden_keys)}"
            )

        object.__setattr__(self, "metadata", freeze_mapping(dict(self.metadata)))
