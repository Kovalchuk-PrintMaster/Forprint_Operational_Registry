from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_checkpoint_b_docs_exist() -> None:
    required_docs = [
        "docs/architecture/lifecycle_validation.md",
        "docs/architecture/operational_blockers.md",
    ]

    for relative_path in required_docs:
        assert (PROJECT_ROOT / relative_path).exists()


def test_blocker_model_does_not_import_foreign_runtime_code() -> None:
    text = (PROJECT_ROOT / "app/forprint_operational_registry/models/blockers.py").read_text()

    import_lines = [
        line.strip().lower()
        for line in text.splitlines()
        if line.strip().startswith(("import ", "from "))
    ]

    forbidden_tokens = [
        "accounting_registry",
        "warehouse",
        "forprint_prepress_hub",
        "forprint_crm",
        "fastapi",
        "requests",
    ]

    for line in import_lines:
        for token in forbidden_tokens:
            assert token not in line


def test_operational_blockers_doc_preserves_boundaries() -> None:
    text = (PROJECT_ROOT / "docs/architecture/operational_blockers.md").read_text()

    assert "Accounting payment truth" in text
    assert "Warehouse reservation truth" in text
    assert "Prepress file lifecycle" in text
    assert "CRM communication history" in text
