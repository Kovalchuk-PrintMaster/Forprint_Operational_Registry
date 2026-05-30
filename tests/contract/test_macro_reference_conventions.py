from forprint_operational_registry.dto.references import (
    AccountingReference,
    CalculatorReference,
    CRMReference,
    GatewayReference,
    LibraryReference,
    PrepressReference,
    TelegramReference,
)


def test_foreign_references_can_be_created_without_importing_foreign_modules() -> None:
    refs = [
        TelegramReference("telegram_chat_001", "telegram_chat_ref"),
        CRMReference("crm_decision_001", "crm_decision_ref"),
        CalculatorReference("quote_001", "calculator_quote_ref"),
        AccountingReference("payment_001", "accounting_payment_ref"),
        PrepressReference("prepress_job_001", "prepress_job_ref"),
        LibraryReference("template_001", "library_template_ref"),
        GatewayReference("correlation_001", "gateway_correlation_ref"),
    ]

    assert refs[0].reference_type == "telegram_chat_ref"
    assert refs[3].source_module == "accounting_registry_future"
    assert refs[6].source_module == "forprint_integration_gateway_future"


def test_references_do_not_become_foreign_domain_ownership() -> None:
    ref = AccountingReference(
        "payment_001",
        "accounting_payment_ref",
        metadata={"note": "reference only"},
    )

    assert ref.reference_id == "payment_001"
    assert ref.metadata["note"] == "reference only"
    assert "payment_truth" not in ref.metadata
