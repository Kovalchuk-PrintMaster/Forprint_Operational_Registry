from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_envelope_does_not_import_gateway_code() -> None:
    text = (PROJECT_ROOT / "app/forprint_operational_registry/dto/envelope.py").read_text()

    import_lines = [
        line.strip().lower()
        for line in text.splitlines()
        if line.strip().startswith(("import ", "from "))
    ]

    forbidden_tokens = [
        "forprint_integration_gateway",
        "gateway.",
        "fastapi",
        "requests",
    ]

    for line in import_lines:
        for token in forbidden_tokens:
            assert token not in line


def test_references_do_not_import_foreign_module_code() -> None:
    text = (PROJECT_ROOT / "app/forprint_operational_registry/dto/references.py").read_text()

    import_lines = [
        line.strip().lower()
        for line in text.splitlines()
        if line.strip().startswith(("import ", "from "))
    ]

    forbidden_tokens = [
        "accounting_registry",
        "calculator_engine",
        "forprint_prepress_hub",
        "forprint_integration_gateway",
        "forprint_crm",
        "telegram",
        "forprint_library",
    ]

    for line in import_lines:
        for token in forbidden_tokens:
            assert token not in line


def test_checkpoint_a_docs_exist() -> None:
    required_docs = [
        "docs/architecture/command_envelope.md",
        "docs/architecture/future_gateway_crm_contracts.md",
        "docs/architecture/reference_conventions.md",
    ]

    for relative_path in required_docs:
        assert (PROJECT_ROOT / relative_path).exists()


def test_no_real_integration_paths_are_added() -> None:
    forbidden_paths = [
        "app/forprint_operational_registry/api",
        "app/forprint_operational_registry/adapters/gateway",
        "app/forprint_operational_registry/adapters/crm",
        "app/forprint_operational_registry/adapters/telegram",
        "app/forprint_operational_registry/http",
    ]

    for relative_path in forbidden_paths:
        assert not (PROJECT_ROOT / relative_path).exists()
