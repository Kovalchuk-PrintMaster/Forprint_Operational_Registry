"""Operational error and warning taxonomy for v0.4."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Any


class OperationalErrorCode(StrEnum):
    """Known operational error codes."""

    VALIDATION_FAILED = "operational.validation_failed"
    INVALID_TRANSITION = "operational.invalid_transition"
    ENTITY_NOT_FOUND = "operational.entity_not_found"
    BLOCKED_BY_ACTIVE_BLOCKER = "operational.blocked_by_active_blocker"
    REFERENCE_MISSING = "operational.reference_missing"
    REFERENCE_INVALID = "operational.reference_invalid"
    DUPLICATE_COMMAND = "operational.duplicate_command"
    CONFLICT = "operational.conflict"
    FORBIDDEN_FOREIGN_OWNERSHIP = "operational.forbidden_foreign_ownership"


class OperationalWarningCode(StrEnum):
    """Known operational warning codes."""

    MISSING_CALCULATION_REFERENCE = "operational.missing_calculation_reference"
    WAITING_PAYMENT_REFERENCE = "operational.waiting_payment_reference"
    WAITING_PREPRESS_REFERENCE = "operational.waiting_prepress_reference"
    MANUAL_REVIEW_RECOMMENDED = "operational.manual_review_recommended"
    USES_PLACEHOLDER_CONTRACT = "operational.uses_placeholder_contract"


def freeze_details(details: Mapping[str, Any]) -> Mapping[str, Any]:
    """Freeze error/warning details."""

    return MappingProxyType(dict(details))


@dataclass(frozen=True, slots=True)
class OperationalError:
    """Structured operational error."""

    code: str
    message: str
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "details", freeze_details(self.details))


@dataclass(frozen=True, slots=True)
class OperationalWarning:
    """Structured operational warning."""

    code: str
    message: str
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "details", freeze_details(self.details))


KNOWN_ERROR_CODES: tuple[str, ...] = tuple(code.value for code in OperationalErrorCode)
KNOWN_WARNING_CODES: tuple[str, ...] = tuple(code.value for code in OperationalWarningCode)
