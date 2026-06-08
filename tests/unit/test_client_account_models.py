from datetime import UTC, datetime

import pytest
from forprint_operational_registry.models.client_account import (
    AccountContactLink,
    ClientAccount,
    ClientAddress,
    ClientBankAccount,
    ClientContract,
    ClientGroup,
    ClientNote,
    ClientPreference,
    ContactMethod,
    ContactPerson,
    CustomerIdentityLookupResult,
    ExternalAccountingReference,
    LegacyClientImportMapping,
    LegalEntityProfile,
)


def test_client_account_can_be_created_and_preserves_legacy_raw_name() -> None:
    account = ClientAccount(
        client_account_id="acc_demo_001",
        account_type="organization",
        display_name="Demo Medical Group",
        legal_name="Demo Legal Entity LLC",
        legacy_raw_name="ТОВ Демо Медікал / old raw card",
    )

    assert account.client_account_id == "acc_demo_001"
    assert account.legacy_raw_name == "ТОВ Демо Медікал / old raw card"


def test_client_group_can_be_created() -> None:
    group = ClientGroup(
        client_group_id="grp_demo_001",
        display_name="Demo Business Group",
    )

    assert group.client_group_id == "grp_demo_001"


def test_legal_entity_profile_links_to_client_account() -> None:
    profile = LegalEntityProfile(
        legal_entity_profile_id="lep_demo_001",
        client_account_id="acc_demo_001",
        legal_entity_type="legal_entity",
        legal_name="Demo Legal Entity LLC",
        edrpou="00000000",
    )

    assert profile.client_account_id == "acc_demo_001"
    assert profile.edrpou == "00000000"


def test_contact_person_can_be_created() -> None:
    person = ContactPerson(
        contact_person_id="cp_demo_001",
        full_name="Demo Contact",
        preferred_name="Demo",
        position="Manager",
    )

    assert person.preferred_name == "Demo"


def test_contact_method_supports_raw_and_normalized_value() -> None:
    method = ContactMethod(
        contact_method_id="cm_demo_001",
        method_type="phone",
        kind="manager",
        raw_value="(050) 000-00-00",
        normalized_value="+380500000000",
    )

    assert method.raw_value == "(050) 000-00-00"
    assert method.normalized_value == "+380500000000"


def test_account_contact_link_supports_valid_from_and_valid_to() -> None:
    valid_from = datetime(2026, 1, 1, tzinfo=UTC)
    valid_to = datetime(2026, 12, 31, tzinfo=UTC)

    link = AccountContactLink(
        account_contact_link_id="acl_demo_001",
        client_account_id="acc_demo_001",
        contact_method_id="cm_demo_001",
        role="manager",
        valid_from=valid_from,
        valid_to=valid_to,
    )

    assert link.valid_from == valid_from
    assert link.valid_to == valid_to


def test_client_address_preserves_raw_presentation() -> None:
    address = ClientAddress(
        client_address_id="addr_demo_001",
        client_account_id="acc_demo_001",
        address_type="delivery",
        raw_presentation="Нова Пошта, demo raw branch text",
        delivery_service="nova_poshta",
    )

    assert "Нова Пошта" in address.raw_presentation


def test_external_accounting_reference_stores_1c_code_and_ref() -> None:
    ref = ExternalAccountingReference(
        external_reference_id="ext_demo_001",
        entity_type="counterparty",
        internal_entity_id="acc_demo_001",
        source_system="1c_bas",
        external_code="000000001",
        external_ref="1c-ref-demo",
        external_name="Demo 1C Counterparty",
        raw_payload={"raw_1c_code": "000000001"},
    )

    assert ref.external_code == "000000001"
    assert ref.raw_payload["raw_1c_code"] == "000000001"


def test_client_contract_links_to_account() -> None:
    contract = ClientContract(
        client_contract_id="contract_demo_001",
        client_account_id="acc_demo_001",
        contract_name="Основний договір",
        contract_type="main",
        settlement_mode="standard",
    )

    assert contract.client_account_id == "acc_demo_001"


def test_client_bank_account_links_to_account() -> None:
    bank = ClientBankAccount(
        client_bank_account_id="bank_demo_001",
        client_account_id="acc_demo_001",
        display_name="Main IBAN",
        bank_name="Demo Bank",
        iban="UA000000000000000000000000000",
    )

    assert bank.iban.startswith("UA")


def test_client_note_supports_note_type() -> None:
    note = ClientNote(
        client_note_id="note_demo_001",
        client_account_id="acc_demo_001",
        note_type="production",
        content="Preserve production memory from legacy comments.",
    )

    assert note.note_type == "production"


def test_client_preference_supports_preference_type() -> None:
    preference = ClientPreference(
        client_preference_id="pref_demo_001",
        client_account_id="acc_demo_001",
        preference_type="preferred_materials",
        value="demo material preference",
    )

    assert preference.preference_type == "preferred_materials"


def test_legacy_import_mapping_preserves_raw_values() -> None:
    mapping = LegacyClientImportMapping(
        legacy_mapping_id="legacy_demo_001",
        source_system="telegram_bot_legacy",
        source_table="clients",
        source_id="legacy_001",
        client_account_id="acc_demo_001",
        raw_name="Raw legacy name",
        raw_phone="Raw legacy phone",
        raw_payload={"telegram_id": "123"},
    )

    assert mapping.raw_name == "Raw legacy name"
    assert mapping.raw_payload["telegram_id"] == "123"


def test_phone_is_not_allowed_as_account_metadata_truth() -> None:
    with pytest.raises(ValueError, match="must not own foreign-domain truth"):
        ClientAccount(
            client_account_id="acc_demo_001",
            account_type="organization",
            display_name="Bad Account",
            metadata={"crm_dashboard_state": "bad"},
        )


def test_customer_identity_lookup_result_supports_ambiguous_status() -> None:
    result = CustomerIdentityLookupResult(
        lookup_status="multiple_matches_manual_review_required",
        matched_client_account_ids=("acc_demo_001", "acc_demo_002"),
        lookup_key="+380500000000",
        lookup_type="normalized_phone",
    )

    assert len(result.matched_client_account_ids) == 2
