"""Client identity lookup helpers.

ClientAccount ID is canonical truth.
Phone/name/1C code are lookup keys only.
Multiple matches must require manual review.
"""

from forprint_operational_registry.models.client_account import (
    AccountContactLink,
    ClientAccount,
    ContactMethod,
    CustomerIdentityLookupResult,
    ExternalAccountingReference,
)


class CustomerIdentityLookupService:
    """Small deterministic lookup helper for ClientAccount foundation."""

    def __init__(
        self,
        accounts: list[ClientAccount],
        contact_methods: list[ContactMethod],
        account_contact_links: list[AccountContactLink],
        external_accounting_references: list[ExternalAccountingReference],
    ) -> None:
        self._accounts = {account.client_account_id: account for account in accounts}
        self._contact_methods = {method.contact_method_id: method for method in contact_methods}
        self._account_contact_links = account_contact_links
        self._external_accounting_references = external_accounting_references

    def lookup_by_normalized_phone(
        self, normalized_phone: str | None
    ) -> CustomerIdentityLookupResult:
        """Lookup ClientAccount by normalized phone.

        Phone is not canonical identity.
        Multiple matches require manual review.
        """

        if not normalized_phone or not normalized_phone.strip():
            return CustomerIdentityLookupResult(
                lookup_status="invalid_lookup_input",
                lookup_key=normalized_phone,
                lookup_type="normalized_phone",
                reason="normalized_phone is empty",
            )

        matching_method_ids = {
            method.contact_method_id
            for method in self._contact_methods.values()
            if method.method_type == "phone"
            and method.normalized_value == normalized_phone
            and method.status == "active"
        }

        matched_account_ids = sorted(
            {
                link.client_account_id
                for link in self._account_contact_links
                if link.contact_method_id in matching_method_ids
                and link.status == "active"
                and link.client_account_id in self._accounts
            }
        )

        return self._build_result(
            matched_account_ids=matched_account_ids,
            lookup_key=normalized_phone,
            lookup_type="normalized_phone",
        )

    def lookup_by_external_1c_code(self, external_code: str | None) -> CustomerIdentityLookupResult:
        """Lookup ClientAccount by external 1C/BAS code reference."""

        if not external_code or not external_code.strip():
            return CustomerIdentityLookupResult(
                lookup_status="invalid_lookup_input",
                lookup_key=external_code,
                lookup_type="external_1c_code",
                reason="external_code is empty",
            )

        matched_account_ids = sorted(
            {
                reference.internal_entity_id
                for reference in self._external_accounting_references
                if reference.source_system in {"1c", "1c_bas", "bas"}
                and reference.entity_type == "counterparty"
                and reference.external_code == external_code
                and reference.internal_entity_id in self._accounts
            }
        )

        return self._build_result(
            matched_account_ids=matched_account_ids,
            lookup_key=external_code,
            lookup_type="external_1c_code",
        )

    def lookup_by_name(self, name: str | None) -> CustomerIdentityLookupResult:
        """Lookup ClientAccount by display/legal/common/legacy name.

        Names are not canonical identity.
        """

        if not name or not name.strip():
            return CustomerIdentityLookupResult(
                lookup_status="invalid_lookup_input",
                lookup_key=name,
                lookup_type="name",
                reason="name is empty",
            )

        normalized_name = name.strip().casefold()

        matched_account_ids = sorted(
            account.client_account_id
            for account in self._accounts.values()
            if normalized_name
            in {
                value.strip().casefold()
                for value in (
                    account.display_name,
                    account.common_name,
                    account.legal_name,
                    account.legacy_raw_name,
                )
                if value
            }
        )

        return self._build_result(
            matched_account_ids=matched_account_ids,
            lookup_key=name,
            lookup_type="name",
        )

    @staticmethod
    def _build_result(
        matched_account_ids: list[str],
        lookup_key: str,
        lookup_type: str,
    ) -> CustomerIdentityLookupResult:
        """Build lookup result with manual-review behavior for ambiguity."""

        if not matched_account_ids:
            return CustomerIdentityLookupResult(
                lookup_status="no_match",
                matched_client_account_ids=(),
                lookup_key=lookup_key,
                lookup_type=lookup_type,
            )

        if len(matched_account_ids) == 1:
            return CustomerIdentityLookupResult(
                lookup_status="single_match",
                matched_client_account_ids=tuple(matched_account_ids),
                lookup_key=lookup_key,
                lookup_type=lookup_type,
            )

        return CustomerIdentityLookupResult(
            lookup_status="multiple_matches_manual_review_required",
            matched_client_account_ids=tuple(matched_account_ids),
            lookup_key=lookup_key,
            lookup_type=lookup_type,
            reason="Multiple ClientAccounts matched; manual account selection is required.",
        )
