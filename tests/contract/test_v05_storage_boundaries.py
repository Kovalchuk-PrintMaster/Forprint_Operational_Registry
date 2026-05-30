from pathlib import Path

from forprint_operational_registry.repositories.factory import create_repository_bundle
from forprint_operational_registry.storage.schema import STORAGE_TABLE_NAMES

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_storage_docs_exist() -> None:
    docs = [
        "docs/storage/storage_strategy.md",
        "docs/storage/sqlite_test_storage.md",
        "docs/storage/postgresql_future_path.md",
        "docs/storage/repository_storage_boundary.md",
        "docs/storage/persistence_safety_rules.md",
    ]

    for doc in docs:
        assert (PROJECT_ROOT / doc).exists()


def test_no_forbidden_foreign_domain_tables_are_introduced() -> None:
    forbidden = {
        "invoices",
        "payments",
        "one_c_snapshots",
        "product_catalog",
        "material_catalog",
        "price_calculations",
        "prepress_files",
        "warehouse_stock",
        "crm_dashboard_state",
        "gateway_routes",
        "library_contracts",
    }

    assert not forbidden.intersection(STORAGE_TABLE_NAMES)


def test_repository_factory_can_create_memory_and_sqlite(tmp_path: Path) -> None:
    memory_bundle = create_repository_bundle("memory")
    sqlite_bundle = create_repository_bundle(
        "sqlite",
        f"sqlite:///{tmp_path / 'factory.sqlite3'}",
    )

    assert hasattr(memory_bundle, "orders")
    assert hasattr(sqlite_bundle, "orders")


def test_repository_factory_rejects_postgresql_in_v05() -> None:
    try:
        create_repository_bundle("postgresql")
    except ValueError as error:
        assert "planned but not implemented" in str(error)
    else:
        raise AssertionError("postgresql backend must not be implemented in v0.5")


def test_storage_layer_does_not_create_api_or_migrations() -> None:
    forbidden_paths = [
        "app/forprint_operational_registry/api",
        "app/forprint_operational_registry/migrations",
        "alembic",
        "alembic.ini",
    ]

    for relative_path in forbidden_paths:
        assert not (PROJECT_ROOT / relative_path).exists()
