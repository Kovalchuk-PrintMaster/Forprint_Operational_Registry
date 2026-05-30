"""Storage configuration for Operational Registry v0.5."""

from dataclasses import dataclass

ALLOWED_STORAGE_BACKENDS: tuple[str, ...] = ("memory", "sqlite")
PLANNED_STORAGE_BACKENDS: tuple[str, ...] = ("postgresql",)


@dataclass(frozen=True, slots=True)
class StorageConfig:
    """Storage backend configuration."""

    backend: str = "memory"
    database_url: str | None = None

    def __post_init__(self) -> None:
        if self.backend not in ALLOWED_STORAGE_BACKENDS:
            raise ValueError(f"Unsupported storage backend in v0.5: {self.backend}")
