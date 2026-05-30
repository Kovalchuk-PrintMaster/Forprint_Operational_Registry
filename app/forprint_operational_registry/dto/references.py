"""Reference DTOs for foreign-domain references.

References are identifiers only.
They must not import or own foreign-domain objects.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any


def freeze_metadata(value: Mapping[str, Any]) -> Mapping[str, Any]:
    """Freeze reference metadata."""

    return MappingProxyType(dict(value))


@dataclass(slots=True)
class ExternalReference:
    """Generic external reference.

    This is not ownership of the foreign object.
    """

    reference_id: str
    reference_type: str
    source_module: str
    source_channel: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.reference_id:
            raise ValueError("reference_id is required")

        if not self.reference_type:
            raise ValueError("reference_type is required")

        if not self.source_module:
            raise ValueError("source_module is required")

        self.metadata = freeze_metadata(self.metadata)


class AccountingReference(ExternalReference):
    """Reference to future Accounting Registry object."""

    def __init__(
        self,
        reference_id: str,
        reference_type: str = "accounting_reference",
        source_channel: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            reference_id=reference_id,
            reference_type=reference_type,
            source_module="accounting_registry_future",
            source_channel=source_channel,
            metadata=metadata or {},
        )


class CalculatorReference(ExternalReference):
    """Reference to future Calculator Engine result."""

    def __init__(
        self,
        reference_id: str,
        reference_type: str = "calculator_reference",
        source_channel: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            reference_id=reference_id,
            reference_type=reference_type,
            source_module="calculator_engine_future",
            source_channel=source_channel,
            metadata=metadata or {},
        )


class PrepressReference(ExternalReference):
    """Reference to future Prepress Hub object."""

    def __init__(
        self,
        reference_id: str,
        reference_type: str = "prepress_reference",
        source_channel: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            reference_id=reference_id,
            reference_type=reference_type,
            source_module="forprint_prepress_hub_future",
            source_channel=source_channel,
            metadata=metadata or {},
        )


class GatewayReference(ExternalReference):
    """Reference to future Integration Gateway envelope or correlation."""

    def __init__(
        self,
        reference_id: str,
        reference_type: str = "gateway_reference",
        source_channel: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            reference_id=reference_id,
            reference_type=reference_type,
            source_module="forprint_integration_gateway_future",
            source_channel=source_channel,
            metadata=metadata or {},
        )


class TelegramReference(ExternalReference):
    """Reference to future Telegram channel object."""

    def __init__(
        self,
        reference_id: str,
        reference_type: str = "telegram_reference",
        source_channel: str | None = "telegram_bot",
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            reference_id=reference_id,
            reference_type=reference_type,
            source_module="telegram_bot_future",
            source_channel=source_channel,
            metadata=metadata or {},
        )


class CRMReference(ExternalReference):
    """Reference to future CRM decision/workspace object."""

    def __init__(
        self,
        reference_id: str,
        reference_type: str = "crm_reference",
        source_channel: str | None = "crm_manual",
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            reference_id=reference_id,
            reference_type=reference_type,
            source_module="forprint_crm_future",
            source_channel=source_channel,
            metadata=metadata or {},
        )


class LibraryReference(ExternalReference):
    """Reference to future Library template/catalog/contract object."""

    def __init__(
        self,
        reference_id: str,
        reference_type: str = "library_reference",
        source_channel: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            reference_id=reference_id,
            reference_type=reference_type,
            source_module="forprint_library_future",
            source_channel=source_channel,
            metadata=metadata or {},
        )
