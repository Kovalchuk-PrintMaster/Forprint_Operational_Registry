"""Operational blocker model.

Blockers are lightweight operational helpers.
They are not Accounting payment truth, Warehouse reservation truth,
Prepress file lifecycle or CRM communication history.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

ALLOWED_OPERATIONAL_BLOCKER_TYPES: tuple[str, ...] = (
    "missing_client_data",
    "missing_calculation",
    "waiting_payment_reference",
    "waiting_prepress_check",
    "waiting_operator_review",
    "material_availability_unknown",
    "manual_review_required",
)

ALLOWED_BLOCKER_STATUSES: tuple[str, ...] = ("open", "resolved")
ALLOWED_BLOCKER_SEVERITIES: tuple[str, ...] = ("low", "medium", "high", "critical")

FORBIDDEN_BLOCKER_METADATA_KEYS: tuple[str, ...] = (
    "payment_truth",
    "invoice_truth",
    "warehouse_reservation_truth",
    "warehouse_stock_balance",
    "prepress_file_lifecycle",
    "uploaded_file_binary_storage",
    "crm_communication_history",
    "customer_chat_archive",
)


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""

    return datetime.now(UTC)


def freeze_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    """Freeze metadata mapping."""

    return MappingProxyType(dict(value))


@dataclass(slots=True)
class OperationalBlocker:
    """Lightweight operational blocker."""

    blocker_id: str
    entity_type: str
    entity_id: str
    blocker_type: str
    reason: str
    source_module: str
    severity: str = "medium"
    status: str = "open"
    created_at: datetime = field(default_factory=utc_now)
    resolved_at: datetime | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.blocker_id:
            raise ValueError("blocker_id is required")

        if not self.entity_type:
            raise ValueError("entity_type is required")

        if not self.entity_id:
            raise ValueError("entity_id is required")

        if self.blocker_type not in ALLOWED_OPERATIONAL_BLOCKER_TYPES:
            raise ValueError(f"Unknown operational blocker type: {self.blocker_type}")

        if not self.reason:
            raise ValueError("reason is required")

        if not self.source_module:
            raise ValueError("source_module is required")

        if self.severity not in ALLOWED_BLOCKER_SEVERITIES:
            raise ValueError(f"Unknown blocker severity: {self.severity}")

        if self.status not in ALLOWED_BLOCKER_STATUSES:
            raise ValueError(f"Unknown blocker status: {self.status}")

        forbidden_keys = set(self.metadata).intersection(FORBIDDEN_BLOCKER_METADATA_KEYS)
        if forbidden_keys:
            raise ValueError(
                "OperationalBlocker must not become foreign-domain truth. "
                f"Forbidden metadata keys: {sorted(forbidden_keys)}"
            )

        self.metadata = freeze_mapping(self.metadata)

    @property
    def blocks_operational_readiness(self) -> bool:
        """Return whether this blocker currently blocks operational readiness."""

        return self.status == "open"

    def resolve(self) -> None:
        """Resolve blocker."""

        if self.status == "resolved":
            return

        self.status = "resolved"
        self.resolved_at = utc_now()
