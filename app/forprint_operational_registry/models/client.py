"""Client model for canonical operational client identity."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

FORBIDDEN_CRM_PROFILE_KEYS: tuple[str, ...] = (
    "full_crm_interaction_history",
    "sales_pipeline",
    "marketing_profile",
    "crm_dashboard_preferences",
    "manager_workspace_state",
    "full_communication_timeline",
)


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""

    return datetime.now(UTC)


@dataclass(slots=True)
class ClientRecord:
    """Canonical operational client identity.

    This model is intentionally not a full CRM profile.
    CRM may own workspace/profile projections later.
    """

    client_id: str
    display_name: str
    contact_refs: list[str] = field(default_factory=list)
    source_refs: dict[str, Any] = field(default_factory=dict)
    status: str = "active"
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.client_id:
            raise ValueError("client_id is required")

        if not self.display_name:
            raise ValueError("display_name is required")

        forbidden_keys = set(self.metadata).intersection(FORBIDDEN_CRM_PROFILE_KEYS)
        if forbidden_keys:
            raise ValueError(
                "ClientRecord must not become CRM profile. "
                f"Forbidden metadata keys: {sorted(forbidden_keys)}"
            )
