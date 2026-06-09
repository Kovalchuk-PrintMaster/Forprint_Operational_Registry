"""Canonical dictionary mapping models.

Operational Registry consumes Library dictionary IDs by reference.
Library remains the semantic authority.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime

MAPPING_STATUSES: tuple[str, ...] = (
    "confirmed",
    "confirmed_with_alias",
    "pending_library_reference",
    "manual_review_required",
    "deprecated_reference",
    "intentionally_local",
    "unresolved",
    "unknown",
)

DICTIONARY_REFERENCE_STATUSES: tuple[str, ...] = (
    "active",
    "deprecated",
    "pending",
    "unknown",
)

DICTIONARY_VERSION_PIN_STATUSES: tuple[str, ...] = (
    "active",
    "superseded",
    "draft",
    "unknown",
)


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""

    return datetime.now(UTC)


def ensure_in(value: str, allowed: tuple[str, ...], field_name: str) -> None:
    """Validate local enum value."""

    if value not in allowed:
        raise ValueError(f"Unknown {field_name}: {value}")


@dataclass(frozen=True, slots=True)
class CanonicalDictionaryReference:
    """Reference to a Library canonical dictionary value."""

    dictionary_reference_id: str
    dictionary_group: str
    canonical_id: str
    library_version: str
    label_snapshot: str | None = None
    status: str = "active"
    source_system: str = "forprint_library"
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.dictionary_reference_id:
            raise ValueError("dictionary_reference_id is required")
        if not self.dictionary_group:
            raise ValueError("dictionary_group is required")
        if not self.canonical_id:
            raise ValueError("canonical_id is required")
        if not self.library_version:
            raise ValueError("library_version is required")
        ensure_in(self.status, DICTIONARY_REFERENCE_STATUSES, "status")


@dataclass(frozen=True, slots=True)
class LocalEnumMapping:
    """Mapping from Operational Registry local value to Library canonical ID."""

    mapping_id: str
    local_group: str
    local_value: str
    library_dictionary_group: str
    library_canonical_id: str | None = None
    mapping_status: str = "unresolved"
    resolution_source: str = "local_mapping_config"
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.mapping_id:
            raise ValueError("mapping_id is required")
        if not self.local_group:
            raise ValueError("local_group is required")
        if not self.local_value:
            raise ValueError("local_value is required")
        if not self.library_dictionary_group:
            raise ValueError("library_dictionary_group is required")
        ensure_in(self.mapping_status, MAPPING_STATUSES, "mapping_status")

        if self.mapping_status in {"confirmed", "confirmed_with_alias"}:
            if not self.library_canonical_id:
                raise ValueError("library_canonical_id is required for confirmed mapping")


@dataclass(frozen=True, slots=True)
class DictionaryVersionPin:
    """Pinned Library dictionary version used by Operational Registry mapping."""

    dictionary_version_pin_id: str
    library_dictionary_version: str
    library_commit_ref: str | None = None
    pinned_at: datetime = field(default_factory=utc_now)
    status: str = "active"
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.dictionary_version_pin_id:
            raise ValueError("dictionary_version_pin_id is required")
        if not self.library_dictionary_version:
            raise ValueError("library_dictionary_version is required")
        ensure_in(self.status, DICTIONARY_VERSION_PIN_STATUSES, "status")


@dataclass(frozen=True, slots=True)
class DictionaryAlignmentResult:
    """Summary of dictionary alignment validation."""

    alignment_result_id: str
    checked_at: datetime
    groups_checked: tuple[str, ...]
    confirmed_count: int
    unresolved_count: int
    deprecated_count: int
    manual_review_count: int
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.alignment_result_id:
            raise ValueError("alignment_result_id is required")
        if self.confirmed_count < 0:
            raise ValueError("confirmed_count must not be negative")
        if self.unresolved_count < 0:
            raise ValueError("unresolved_count must not be negative")
        if self.deprecated_count < 0:
            raise ValueError("deprecated_count must not be negative")
        if self.manual_review_count < 0:
            raise ValueError("manual_review_count must not be negative")
