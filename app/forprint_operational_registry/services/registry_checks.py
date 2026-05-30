"""Internal validation checks for Operational Registry bootstrap."""

from pathlib import Path
from typing import Any

import yaml

REQUIRED_DOCS: tuple[str, ...] = (
    "docs/architecture/operational_registry_boundaries.md",
    "docs/architecture/operational_vs_accounting_registry.md",
    "docs/architecture/operational_vs_crm.md",
    "docs/architecture/order_lifecycle_v0.md",
    "docs/architecture/command_query_boundary.md",
    "docs/architecture/repository_boundary.md",
    "docs/architecture/service_layer.md",
    "docs/architecture/future_integration_contracts.md",
    "docs/architecture/operational_notes.md",
)

REQUIRED_MUST_NOT_OWN: tuple[str, ...] = (
    "invoice",
    "payment",
    "accounting_document",
    "one_c_raw_snapshot",
    "material_catalog",
    "product_catalog",
    "price_calculation",
    "prepress_file_lifecycle",
    "uploaded_file_binary_storage",
    "warehouse_stock_balance",
    "integration_routing",
    "library_contract_registry",
    "architecture_governance",
)

REQUIRED_ORDER_STATUSES: tuple[str, ...] = (
    "new",
    "needs_review",
    "quote_pending",
    "quote_accepted",
    "payment_reference_pending",
    "payment_reference_confirmed",
    "in_prepress",
    "ready_for_production",
    "in_production",
    "ready_for_pickup",
    "completed",
    "cancelled",
    "blocked",
)

RECOMMENDED_SOURCE_CHANNELS: tuple[str, ...] = (
    "telegram_bot",
    "website",
    "mobile_app",
    "crm_manual",
    "gateway_import",
    "internal_module",
    "legacy_import",
)

REQUIRED_V02_FILES: tuple[str, ...] = (
    "app/forprint_operational_registry/dto/commands.py",
    "app/forprint_operational_registry/dto/queries.py",
    "app/forprint_operational_registry/repositories/interfaces.py",
    "app/forprint_operational_registry/repositories/memory.py",
    "app/forprint_operational_registry/models/note.py",
    "app/forprint_operational_registry/services/client_registry.py",
    "app/forprint_operational_registry/services/order_registry.py",
    "app/forprint_operational_registry/services/task_registry.py",
    "app/forprint_operational_registry/services/event_registry.py",
    "app/forprint_operational_registry/services/note_registry.py",
    "app/forprint_operational_registry/services/order_queries.py",
)

FORBIDDEN_PRODUCTION_API_PATHS: tuple[str, ...] = (
    "app/forprint_operational_registry/api",
    "app/forprint_operational_registry/routes",
    "app/forprint_operational_registry/routers",
    "app/forprint_operational_registry/http",
)


def load_yaml(path: Path) -> dict[str, Any]:
    """Load YAML file as dictionary."""

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")

    return data


def validate_manifest(project_root: Path) -> list[str]:
    """Validate module manifest and boundary ownership."""

    errors: list[str] = []
    manifest_path = project_root / "forprint_module_manifest.yaml"

    if not manifest_path.exists():
        return ["forprint_module_manifest.yaml is missing"]

    manifest = load_yaml(manifest_path)

    if manifest.get("module_id") != "forprint_operational_registry":
        errors.append("manifest module_id must be forprint_operational_registry")

    if manifest.get("role") != "operational_truth_registry":
        errors.append("manifest role must be operational_truth_registry")

    must_not_own = set(manifest.get("must_not_own", []))
    for item in REQUIRED_MUST_NOT_OWN:
        if item not in must_not_own:
            errors.append(f"manifest must_not_own is missing: {item}")

    return errors


def validate_required_docs(project_root: Path) -> list[str]:
    """Validate required architecture documents exist."""

    errors: list[str] = []

    for relative_path in REQUIRED_DOCS:
        if not (project_root / relative_path).exists():
            errors.append(f"required architecture doc is missing: {relative_path}")

    return errors


def validate_status_config(project_root: Path) -> list[str]:
    """Validate status config respects Blueprint v0.1/v0.2 terminology."""

    errors: list[str] = []
    status_path = project_root / "app/forprint_operational_registry/config/statuses.yaml"

    if not status_path.exists():
        return ["status config is missing"]

    config = load_yaml(status_path)
    order_statuses = set(config.get("order_statuses", []))

    if "paid" in order_statuses:
        errors.append("paid must not be used as canonical Operational Registry status")

    for status in REQUIRED_ORDER_STATUSES:
        if status not in order_statuses:
            errors.append(f"order status is missing: {status}")

    source_channels = set(config.get("recommended_source_channels", []))
    for channel in RECOMMENDED_SOURCE_CHANNELS:
        if channel not in source_channels:
            errors.append(f"recommended source channel is missing: {channel}")

    return errors


def validate_v02_boundary_files(project_root: Path) -> list[str]:
    """Validate v0.2 command/query/repository/service files exist."""

    errors: list[str] = []

    for relative_path in REQUIRED_V02_FILES:
        if not (project_root / relative_path).exists():
            errors.append(f"required v0.2 boundary file is missing: {relative_path}")

    return errors


def validate_no_production_api(project_root: Path) -> list[str]:
    """Validate v0.2 did not introduce production API paths."""

    errors: list[str] = []

    for relative_path in FORBIDDEN_PRODUCTION_API_PATHS:
        if (project_root / relative_path).exists():
            errors.append(f"production API path is not approved in v0.2: {relative_path}")

    return errors
