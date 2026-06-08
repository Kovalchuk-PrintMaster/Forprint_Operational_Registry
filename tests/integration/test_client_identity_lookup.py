from forprint_operational_registry.models.client_account import (
    AccountContactLink,
    ClientAccount,
    ContactMethod,
    ExternalAccountingReference,
)
from forprint_operational_registry.services.client_identity_lookup import (
    CustomerIdentityLookupService,
)


def test_lookup_by_normalized_phone_returns_single_match() -> None:
    service = CustomerIdentityLookupService(
        accounts=[
            ClientAccount(
                client_account_id="acc_demo_001",
                account_type="organization",
                display_name="Demo Account",
            )
        ],
        contact_methods=[
            ContactMethod(
                contact_method_id="cm_demo_001",
                method_type="phone",
                kind="manager",
                raw_value="+380 XX XXX XX XX",
                normalized_value="+380XXXXXXXXX",
            )
        ],
        account_contact_links=[
            AccountContactLink(
                account_contact_link_id="acl_demo_001",
                client_account_id="acc_demo_001",
                contact_method_id="cm_demo_001",
            )
        ],
        external_accounting_references=[],
    )

    result = service.lookup_by_normalized_phone("+380XXXXXXXXX")

    assert result.lookup_status == "single_match"
    assert result.matched_client_account_ids == ("acc_demo_001",)


def test_same_phone_can_match_multiple_accounts_and_requires_manual_review() -> None:
    service = CustomerIdentityLookupService(
        accounts=[
            ClientAccount(
                client_account_id="acc_demo_001",
                account_type="organization",
                display_name="Demo Company",
            ),
            ClientAccount(
                client_account_id="acc_demo_002",
                account_type="fop",
                display_name="Demo FOP",
            ),
        ],
        contact_methods=[
            ContactMethod(
                contact_method_id="cm_shared_001",
                method_type="phone",
                kind="manager",
                raw_value="+380 ZZ ZZZ ZZ ZZ",
                normalized_value="+380ZZZZZZZZZ",
            )
        ],
        account_contact_links=[
            AccountContactLink(
                account_contact_link_id="acl_demo_001",
                client_account_id="acc_demo_001",
                contact_method_id="cm_shared_001",
            ),
            AccountContactLink(
                account_contact_link_id="acl_demo_002",
                client_account_id="acc_demo_002",
                contact_method_id="cm_shared_001",
            ),
        ],
        external_accounting_references=[],
    )

    result = service.lookup_by_normalized_phone("+380ZZZZZZZZZ")

    assert result.lookup_status == "multiple_matches_manual_review_required"
    assert result.matched_client_account_ids == ("acc_demo_001", "acc_demo_002")


def test_lookup_by_external_1c_code_returns_single_match() -> None:
    service = CustomerIdentityLookupService(
        accounts=[
            ClientAccount(
                client_account_id="acc_demo_001",
                account_type="organization",
                display_name="Demo Account",
            )
        ],
        contact_methods=[],
        account_contact_links=[],
        external_accounting_references=[
            ExternalAccountingReference(
                external_reference_id="ext_demo_001",
                entity_type="counterparty",
                internal_entity_id="acc_demo_001",
                source_system="1c_bas",
                external_code="000000001",
            )
        ],
    )

    result = service.lookup_by_external_1c_code("000000001")

    assert result.lookup_status == "single_match"
    assert result.matched_client_account_ids == ("acc_demo_001",)


def test_lookup_by_display_name_returns_single_match_but_name_is_not_truth() -> None:
    service = CustomerIdentityLookupService(
        accounts=[
            ClientAccount(
                client_account_id="acc_demo_001",
                account_type="organization",
                display_name="Demo Account",
                legal_name="Demo Legal Entity LLC",
            )
        ],
        contact_methods=[],
        account_contact_links=[],
        external_accounting_references=[],
    )

    result = service.lookup_by_name("Demo Account")

    assert result.lookup_status == "single_match"
    assert result.lookup_type == "name"
    assert result.matched_client_account_ids == ("acc_demo_001",)


def test_lookup_returns_no_match_and_invalid_input() -> None:
    service = CustomerIdentityLookupService(
        accounts=[],
        contact_methods=[],
        account_contact_links=[],
        external_accounting_references=[],
    )

    assert service.lookup_by_normalized_phone("+380NOPE").lookup_status == "no_match"
    assert service.lookup_by_normalized_phone("").lookup_status == "invalid_lookup_input"
