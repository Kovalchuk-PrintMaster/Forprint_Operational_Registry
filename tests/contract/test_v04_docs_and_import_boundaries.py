from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_v04_integration_docs_exist() -> None:
    docs = [
        "docs/integration/public_operational_surface.md",
        "docs/integration/command_result_model.md",
        "docs/integration/reference_ready_contracts.md",
        "docs/integration/dependent_module_usage.md",
        "docs/integration/versioning_and_compatibility.md",
    ]

    for doc in docs:
        assert (PROJECT_ROOT / doc).exists()


def test_facade_does_not_import_external_project_modules() -> None:
    text = (
        PROJECT_ROOT / "app/forprint_operational_registry/services/operational_registry_facade.py"
    ).read_text()

    import_lines = [
        line.strip().lower()
        for line in text.splitlines()
        if line.strip().startswith(("import ", "from "))
    ]

    forbidden = [
        "forprint_integration_gateway",
        "forprint_crm",
        "telegram_bot",
        "accounting_registry",
        "calculator_engine",
        "forprint_prepress_hub",
        "fastapi",
        "requests",
    ]

    for line in import_lines:
        for token in forbidden:
            assert token not in line
