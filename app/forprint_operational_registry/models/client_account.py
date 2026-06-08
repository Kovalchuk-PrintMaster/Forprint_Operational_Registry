"""ClientAccount card foundation models.

These models define the first normalized customer/account foundation for ForPrint.

ClientAccount is canonical operational customer/account truth.
Phone, Telegram username, human name and 1C code are lookup/reference values only.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

DRAFT_LOCAL_ENUM_STATUS = "draft_local_until_library_canonicalizes"

ACCOUNT_TYPES: tuple[str, ...] = (
    "person",
    "fop",
    "organization",
    "unknown",
)

CONTACT_METHOD_TYPES: tuple[str, ...] = (
    "phone",
    "email",
    "telegram",
    "viber",
    "web",
    "other",
    "unknown",
)

CONTACT_METHOD_KINDS: tuple[str, ...] = (
    "manager",
    "accounting",
    "main",
    "fax",
    "telegram",
    "unknown",
)

ADDRESS_TYPES: tuple[str, ...] = (
    "legal",
    "actual",
    "delivery",
    "postal",
    "nova_poshta",
    "other",
    "unknown",
)

LEGAL_ENTITY_TYPES: tuple[str, ...] = (
    "physical_person",
    "fop",
    "legal_entity",
    "non_resident",
    "unknown",
)

EXTERNAL_REFERENCE_ENTITY_TYPES: tuple[str, ...] = (
    "counterparty",
    "contract",
    "bank_account",
    "contact_person",
    "address",
    "unknown",
)

CLIENT_NOTE_TYPES: tuple[str, ...] = (
    "internal",
    "sales",
    "accounting",
    "production",
    "logistics",
    "legacy_comment",
    "unknown",
)

CLIENT_PREFERENCE_TYPES: tuple[str, ...] = (
    "communication_style",
    "preferred_carrier",
    "preferred_materials",
    "payment_preference",
    "production_preference",
    "unknown",
)

LOOKUP_STATUSES: tuple[str, ...] = (
    "single_match",
    "multiple_matches_manual_review_required",
    "no_match",
    "invalid_lookup_input",
)

FORBIDDEN_CLIENT_ACCOUNT_FIELDS: tuple[str, ...] = (
    "product_catalog_truth",
    "material_catalog_truth",
    "calculator_pricing_logic",
    "real_accounting_posting",
    "live_1c_sync",
    "crm_dashboard_state",
    "telegram_runtime_ui",
    "prepress_file_lifecycle",
    "warehouse_stock_truth",
)


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""

    return datetime.now(UTC)


def freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    """Freeze mapping for safer DTO/domain usage."""

    return MappingProxyType(dict(value or {}))


def ensure_in(value: str, allowed: tuple[str, ...], field_name: str) -> str:
    """Validate draft-local enum value."""

    if value not in allowed:
        raise ValueError(f"Unknown {field_name}: {value}")

    return value


def ensure_no_forbidden_metadata(metadata: Mapping[str, Any]) -> None:
    """Reject obvious foreign-domain ownership markers."""

    forbidden_keys = set(metadata).intersection(FORBIDDEN_CLIENT_ACCOUNT_FIELDS)
    if forbidden_keys:
        raise ValueError(
            "ClientAccount foundation must not own foreign-domain truth. "
            f"Forbidden metadata keys: {sorted(forbidden_keys)}"
        )


@dataclass(slots=True)
class ClientAccount:
    """Main customer/account/counterparty entity inside ForPrint."""

    client_account_id: str
    account_type: str
    display_name: str
    common_name: str | None = None
    legal_name: str | None = None
    status: str = "active"
    client_group_id: str | None = None
    is_customer: bool = True
    is_supplier: bool = False
    is_resident: bool = True
    primary_contact_method_id: str | None = None
    primary_address_id: str | None = None
    source_system: str = "manual"
    legacy_raw_name: str | None = None
    notes: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.client_account_id:
            raise ValueError("client_account_id is required")

        ensure_in(self.account_type, ACCOUNT_TYPES, "account_type")

        if not self.display_name:
            raise ValueError("display_name is required")

        ensure_no_forbidden_metadata(self.metadata)
        self.metadata = freeze_mapping(self.metadata)


@dataclass(slots=True)
class ClientGroup:
    """Corporate/grouping entity for analytics and grouping."""

    client_group_id: str
    display_name: str
    legal_group_name: str | None = None
    status: str = "active"
    notes: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.client_group_id:
            raise ValueError("client_group_id is required")

        if not self.display_name:
            raise ValueError("display_name is required")


@dataclass(slots=True)
class ContactPerson:
    """Human contact person."""

    contact_person_id: str
    full_name: str
    preferred_name: str | None = None
    position: str | None = None
    status: str = "active"
    notes: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.contact_person_id:
            raise ValueError("contact_person_id is required")

        if not self.full_name:
            raise ValueError("full_name is required")


@dataclass(slots=True)
class ContactMethod:
    """Phone/email/telegram/web/other contact method.

    A contact method is a lookup/contact key, not canonical account identity.
    """

    contact_method_id: str
    method_type: str
    kind: str
    raw_value: str
    normalized_value: str | None = None
    presentation: str | None = None
    is_primary: bool = False
    status: str = "active"
    source_system: str = "manual"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.contact_method_id:
            raise ValueError("contact_method_id is required")

        ensure_in(self.method_type, CONTACT_METHOD_TYPES, "method_type")
        ensure_in(self.kind, CONTACT_METHOD_KINDS, "kind")

        if not self.raw_value:
            raise ValueError("raw_value is required")


@dataclass(slots=True)
class AccountContactLink:
    """Time-aware relationship between account, contact person and/or method."""

    account_contact_link_id: str
    client_account_id: str
    contact_person_id: str | None = None
    contact_method_id: str | None = None
    role: str = "unknown"
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    is_primary: bool = False
    status: str = "active"
    source_system: str = "manual"
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.account_contact_link_id:
            raise ValueError("account_contact_link_id is required")

        if not self.client_account_id:
            raise ValueError("client_account_id is required")

        if not self.contact_person_id and not self.contact_method_id:
            raise ValueError("contact_person_id or contact_method_id is required")


@dataclass(slots=True)
class ClientAddress:
    """Client address with raw presentation preservation."""

    client_address_id: str
    client_account_id: str
    address_type: str
    raw_presentation: str
    normalized_address: str | None = None
    delivery_service: str | None = None
    delivery_notes: str | None = None
    is_primary: bool = False
    status: str = "active"
    source_system: str = "manual"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.client_address_id:
            raise ValueError("client_address_id is required")

        if not self.client_account_id:
            raise ValueError("client_account_id is required")

        ensure_in(self.address_type, ADDRESS_TYPES, "address_type")

        if not self.raw_presentation:
            raise ValueError("raw_presentation is required")


@dataclass(slots=True)
class LegalEntityProfile:
    """Legal/tax profile linked to ClientAccount."""

    legal_entity_profile_id: str
    client_account_id: str
    legal_entity_type: str
    legal_name: str
    edrpou: str | None = None
    tax_id: str | None = None
    vat_number: str | None = None
    tax_scheme: str | None = None
    registration_country: str = "UA"
    is_vat_payer: bool | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.legal_entity_profile_id:
            raise ValueError("legal_entity_profile_id is required")

        if not self.client_account_id:
            raise ValueError("client_account_id is required")

        ensure_in(self.legal_entity_type, LEGAL_ENTITY_TYPES, "legal_entity_type")

        if not self.legal_name:
            raise ValueError("legal_name is required")


@dataclass(slots=True)
class ClientContract:
    """Client contract relationship, 1C/BAS-compatible by references."""

    client_contract_id: str
    client_account_id: str
    contract_name: str
    contract_type: str
    settlement_mode: str
    contract_number: str | None = None
    contract_date: datetime | None = None
    our_legal_entity_ref: str | None = None
    status: str = "active"
    source_system: str = "manual"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.client_contract_id:
            raise ValueError("client_contract_id is required")

        if not self.client_account_id:
            raise ValueError("client_account_id is required")

        if not self.contract_name:
            raise ValueError("contract_name is required")


@dataclass(slots=True)
class ClientBankAccount:
    """Client bank account reference/details."""

    client_bank_account_id: str
    client_account_id: str
    display_name: str
    bank_name: str
    iban: str | None = None
    account_number: str | None = None
    is_primary: bool = False
    status: str = "active"
    source_system: str = "manual"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.client_bank_account_id:
            raise ValueError("client_bank_account_id is required")

        if not self.client_account_id:
            raise ValueError("client_account_id is required")

        if not self.display_name:
            raise ValueError("display_name is required")


@dataclass(slots=True)
class ExternalAccountingReference:
    """Reference to 1C/BAS or other accounting system object.

    This is not ForPrint primary identity.
    """

    external_reference_id: str
    entity_type: str
    internal_entity_id: str
    source_system: str
    external_code: str
    external_ref: str | None = None
    external_name: str | None = None
    sync_status: str = "seen"
    last_seen_at: datetime | None = None
    last_imported_at: datetime | None = None
    last_exported_at: datetime | None = None
    raw_payload: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.external_reference_id:
            raise ValueError("external_reference_id is required")

        ensure_in(self.entity_type, EXTERNAL_REFERENCE_ENTITY_TYPES, "entity_type")

        if not self.internal_entity_id:
            raise ValueError("internal_entity_id is required")

        if not self.source_system:
            raise ValueError("source_system is required")

        if not self.external_code:
            raise ValueError("external_code is required")

        self.raw_payload = freeze_mapping(self.raw_payload)


@dataclass(slots=True)
class ClientPreference:
    """Operational/client preference."""

    client_preference_id: str
    client_account_id: str
    preference_type: str
    value: str
    source_system: str = "manual"
    status: str = "active"
    notes: str | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.client_preference_id:
            raise ValueError("client_preference_id is required")

        if not self.client_account_id:
            raise ValueError("client_account_id is required")

        ensure_in(self.preference_type, CLIENT_PREFERENCE_TYPES, "preference_type")


@dataclass(slots=True)
class ClientNote:
    """Client/account note preserving business and legacy comments."""

    client_note_id: str
    client_account_id: str
    note_type: str
    content: str
    source_system: str = "manual"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.client_note_id:
            raise ValueError("client_note_id is required")

        if not self.client_account_id:
            raise ValueError("client_account_id is required")

        ensure_in(self.note_type, CLIENT_NOTE_TYPES, "note_type")

        if not self.content:
            raise ValueError("content is required")


@dataclass(slots=True)
class LegacyClientImportMapping:
    """Mapping from legacy/Telegram/1C raw records to ClientAccount."""

    legacy_mapping_id: str
    source_system: str
    source_table: str
    source_id: str
    client_account_id: str
    raw_name: str | None = None
    raw_phone: str | None = None
    raw_payload: Mapping[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.legacy_mapping_id:
            raise ValueError("legacy_mapping_id is required")

        if not self.source_system:
            raise ValueError("source_system is required")

        if not self.source_id:
            raise ValueError("source_id is required")

        if not self.client_account_id:
            raise ValueError("client_account_id is required")

        self.raw_payload = freeze_mapping(self.raw_payload)


@dataclass(frozen=True, slots=True)
class CustomerIdentityLookupResult:
    """Deterministic identity lookup result.

    Multiple matches must route to manual review, not auto-selection.
    """

    lookup_status: str
    matched_client_account_ids: tuple[str, ...] = ()
    lookup_key: str | None = None
    lookup_type: str | None = None
    reason: str | None = None

    def __post_init__(self) -> None:
        ensure_in(self.lookup_status, LOOKUP_STATUSES, "lookup_status")
