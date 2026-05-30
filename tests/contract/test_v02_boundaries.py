from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_no_production_api_is_introduced() -> None:
    forbidden_paths = [
        "app/forprint_operational_registry/api",
        "app/forprint_operational_registry/routes",
        "app/forprint_operational_registry/routers",
        "app/forprint_operational_registry/http",
    ]

    for relative_path in forbidden_paths:
        assert not (PROJECT_ROOT / relative_path).exists()


def test_no_foreign_runtime_imports_in_dto_layer() -> None:
    dto_text = (PROJECT_ROOT / "app/forprint_operational_registry/dto/commands.py").read_text()

    import_lines = [
        line.strip().lower()
        for line in dto_text.splitlines()
        if line.strip().startswith(("import ", "from "))
    ]

    forbidden_import_tokens = [
        "fastapi",
        "requests",
        "telegram",
        "crm",
        "gateway",
        "accounting_registry",
        "calculator_engine",
    ]

    for line in import_lines:
        for token in forbidden_import_tokens:
            assert token not in line


def test_v02_docs_state_no_real_integrations() -> None:
    text = (PROJECT_ROOT / "docs/architecture/future_integration_contracts.md").read_text()

    assert "Current v0.2 does not implement real integrations" in text
    assert "network calls" in text
    assert "API calls" in text


def test_repository_boundary_docs_defer_postgresql() -> None:
    text = (PROJECT_ROOT / "docs/architecture/repository_boundary.md").read_text()

    assert "PostgreSQL production storage" in text
    assert "database migrations" in text
