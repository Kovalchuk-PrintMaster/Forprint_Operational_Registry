"""Future-facing local command envelope for Operational Registry.

This envelope is not Gateway.
It does not route commands.
It does not perform transport validation.
It only normalizes a future command shape for internal Operational Registry services.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

from forprint_operational_registry.dto.commands import (
    ChangeOrderStatusCommand,
    CreateOrderCommand,
)


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""

    return datetime.now(UTC)


def freeze_payload(value: Any) -> Any:
    """Recursively freeze dictionaries/lists to avoid accidental mutation."""

    if isinstance(value, dict):
        return MappingProxyType({key: freeze_payload(item) for key, item in value.items()})

    if isinstance(value, list):
        return tuple(freeze_payload(item) for item in value)

    return value


@dataclass(frozen=True, slots=True)
class OperationalCommandEnvelope:
    """Local future-facing command envelope.

    The envelope is internal/offline in v0.3 and must not become transport routing.
    """

    command_id: str
    correlation_id: str
    idempotency_key: str
    source_module: str
    source_channel: str
    actor_ref: str
    target_entity_type: str
    target_entity_id: str
    command_type: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.command_id:
            raise ValueError("command_id is required")

        if not self.correlation_id:
            raise ValueError("correlation_id is required")

        if not self.idempotency_key:
            raise ValueError("idempotency_key is required")

        if not self.source_module:
            raise ValueError("source_module is required")

        if not self.source_channel:
            raise ValueError("source_channel is required")

        if not self.actor_ref:
            raise ValueError("actor_ref is required")

        if not self.target_entity_type:
            raise ValueError("target_entity_type is required")

        if not self.target_entity_id:
            raise ValueError("target_entity_id is required")

        if not self.command_type:
            raise ValueError("command_type is required")

        object.__setattr__(self, "payload", freeze_payload(dict(self.payload)))
        object.__setattr__(self, "metadata", freeze_payload(dict(self.metadata)))

    def to_create_order_command(self) -> CreateOrderCommand:
        """Convert compatible envelope to CreateOrderCommand."""

        if self.command_type != "operational.create_order.v1":
            raise ValueError(
                "Envelope command_type must be operational.create_order.v1 "
                "to convert into CreateOrderCommand"
            )

        if self.target_entity_type != "order":
            raise ValueError("CreateOrderCommand envelope target_entity_type must be order")

        payload = dict(self.payload)

        if "client_id" not in payload:
            raise ValueError("CreateOrderCommand payload must include client_id")

        return CreateOrderCommand(
            order_id=str(payload.get("order_id", self.target_entity_id)),
            client_id=str(payload["client_id"]),
            source_channel=str(payload.get("source_channel", self.source_channel)),
            source_refs=dict(payload.get("source_refs", {})),
            quote_ref=payload.get("quote_ref"),
            calculator_result_ref=payload.get("calculator_result_ref"),
            accounting_refs=dict(payload.get("accounting_refs", {})),
            production_refs=dict(payload.get("production_refs", {})),
            prepress_refs=dict(payload.get("prepress_refs", {})),
            metadata=dict(payload.get("metadata", {})),
            actor_ref=self.actor_ref,
            source_module=self.source_module,
        )

    def to_change_order_status_command(self) -> ChangeOrderStatusCommand:
        """Convert compatible envelope to ChangeOrderStatusCommand."""

        if self.command_type != "operational.change_order_status.v1":
            raise ValueError(
                "Envelope command_type must be operational.change_order_status.v1 "
                "to convert into ChangeOrderStatusCommand"
            )

        if self.target_entity_type != "order":
            raise ValueError("ChangeOrderStatusCommand envelope target_entity_type must be order")

        payload = dict(self.payload)

        if "to_status" not in payload:
            raise ValueError("ChangeOrderStatusCommand payload must include to_status")

        return ChangeOrderStatusCommand(
            order_id=str(payload.get("order_id", self.target_entity_id)),
            to_status=str(payload["to_status"]),
            actor_ref=self.actor_ref,
            source_module=self.source_module,
            reason=payload.get("reason"),
            metadata=dict(payload.get("metadata", {})),
        )
