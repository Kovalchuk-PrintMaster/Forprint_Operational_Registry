from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_client_account_architecture_docs_exist() -> None:
    docs = [
        "docs/architecture/client_account_card_foundation.md",
        "docs/architecture/client_account_1c_compatibility.md",
        "docs/architecture/client_identity_lookup_policy.md",
        "docs/architecture/contact_method_policy.md",
    ]

    for doc in docs:
        assert (PROJECT_ROOT / doc).exists()


def test_client_account_model_does_not_import_foreign_runtime_modules() -> None:
    text = (PROJECT_ROOT / "app/forprint_operational_registry/models/client_account.py").read_text(
        encoding="utf-8"
    )

    import_lines = [
        line.strip().lower()
        for line in text.splitlines()
        if line.strip().startswith(("import ", "from "))
    ]

    forbidden_tokens = [
        "calculator_engine",
        "accounting_registry",
        "forprint_crm",
        "telegram_bot",
        "forprint_prepress_hub",
        "warehouse",
        "fastapi",
        "requests",
    ]

    for line in import_lines:
        for token in forbidden_tokens:
            assert token not in line


def test_client_account_docs_state_canonical_identity_policy() -> None:
    text = (PROJECT_ROOT / "docs/architecture/client_identity_lookup_policy.md").read_text(
        encoding="utf-8"
    )

    assert "client_account_id = canonical truth" in text
    assert "Phone is a strong lookup key but not canonical identity" in text
    assert "multiple_matches_manual_review_required" in text


def test_client_account_1c_doc_preserves_forprint_primary_identity() -> None:
    text = (PROJECT_ROOT / "docs/architecture/client_account_1c_compatibility.md").read_text(
        encoding="utf-8"
    )

    assert "ForPrint primary identity = client_account_id" in text
    assert "ExternalAccountingReference" in text
    assert "No live 1C write" in text
