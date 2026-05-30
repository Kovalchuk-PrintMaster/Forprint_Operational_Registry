"""Repository bundle factory for Operational Registry v0.5."""

from pathlib import Path
from typing import Any

from forprint_operational_registry.repositories.memory import InMemoryRepositoryBundle
from forprint_operational_registry.repositories.sqlite import SQLiteRepositoryBundle


def sqlite_path_from_url(database_url: str | None) -> str:
    """Convert minimal sqlite URL to path."""

    if not database_url:
        return ":memory:"

    if database_url == "sqlite:///:memory:":
        return ":memory:"

    if database_url.startswith("sqlite:///"):
        return database_url.removeprefix("sqlite:///")

    raise ValueError(f"Unsupported database_url for v0.5: {database_url}")


def create_repository_bundle(
    storage_backend: str = "memory",
    database_url: str | None = None,
) -> Any:
    """Create repository bundle for selected backend."""

    if storage_backend == "memory":
        return InMemoryRepositoryBundle()

    if storage_backend == "sqlite":
        return SQLiteRepositoryBundle(Path(sqlite_path_from_url(database_url)))

    if storage_backend == "postgresql":
        raise ValueError("PostgreSQL backend is planned but not implemented in v0.5")

    raise ValueError(f"Unknown storage backend: {storage_backend}")
