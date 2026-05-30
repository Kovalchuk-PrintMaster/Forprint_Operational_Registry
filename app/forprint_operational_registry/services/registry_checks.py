"""Internal validation checks for Operational Registry bootstrap."""

import json
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
    "docs/architecture/command_envelope.md",
    "docs/architecture/future_gateway_crm_contracts.md",
    "docs/architecture/reference_conventions.md",
    "docs/architecture/operational_projections.md",
    "docs/architecture/reporting_readiness.md",
    "docs/architecture/handoff_readiness.md",
    "docs/architecture/module_reference_conventions.md",
    "docs/architecture/order_readiness.md",
    "docs/integration/public_operational_surface.md",
    "docs/integration/command_result_model.md",
    "docs/integration/reference_ready_contracts.md",
    "docs/integration/dependent_module_usage.md",
    "docs/integration/versioning_and_compatibility.md",
)

REQUIRED_MACRO_PACK_FILES: tuple[str, ...] = (
    "app/forprint_operational_registry/dto/projections.py",
    "app/forprint_operational_registry/services/projections.py",
    "app/forprint_operational_registry/services/order_readiness.py",
    "scripts/export_module_status.py",
    "docs/architecture/operational_projections.md",
    "docs/architecture/reporting_readiness.md",
    "docs/architecture/handoff_readiness.md",
    "docs/architecture/module_reference_conventions.md",
    "docs/architecture/order_readiness.md",
)

REQUIRED_HANDOFF_FIXTURES: tuple[str, ...] = (
    "telegram_order_intake_to_create_order.json",
    "crm_manual_order_to_create_order.json",
    "calculator_quote_ref_attached_to_order.json",
    "accounting_payment_reference_update.json",
    "prepress_blocker_attached_to_order.json",
)

REQUIRED_PROJECTION_FIXTURES: tuple[str, ...] = (
    "order_state_projection_example.json",
    "task_board_projection_example.json",
    "operational_timeline_projection_example.json",
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

REQUIRED_CHECKPOINT_A_FILES: tuple[str, ...] = (
    "app/forprint_operational_registry/dto/envelope.py",
    "app/forprint_operational_registry/dto/references.py",
    "docs/architecture/command_envelope.md",
    "docs/architecture/future_gateway_crm_contracts.md",
    "docs/architecture/reference_conventions.md",
)

REQUIRED_CHECKPOINT_B_FILES: tuple[str, ...] = (
    "app/forprint_operational_registry/models/blockers.py",
    "app/forprint_operational_registry/services/blocker_registry.py",
    "docs/architecture/lifecycle_validation.md",
    "docs/architecture/operational_blockers.md",
)

REQUIRED_BLOCKER_TYPES: tuple[str, ...] = (
    "missing_client_data",
    "missing_calculation",
    "waiting_payment_reference",
    "waiting_prepress_check",
    "waiting_operator_review",
    "material_availability_unknown",
    "manual_review_required",
)

REQUIRED_PLACEHOLDER_CONTRACTS: tuple[str, ...] = (
    "operational.create_order.v1.yaml",
    "operational.change_order_status.v1.yaml",
    "operational.create_task.v1.yaml",
    "operational.assign_task.v1.yaml",
    "operational.add_note.v1.yaml",
    "operational.order_state_snapshot.v1.yaml",
    "operational.order_history_snapshot.v1.yaml",
)

FORBIDDEN_PRODUCTION_API_PATHS: tuple[str, ...] = (
    "app/forprint_operational_registry/api",
    "app/forprint_operational_registry/routes",
    "app/forprint_operational_registry/routers",
    "app/forprint_operational_registry/http",
)

FORBIDDEN_REAL_INTEGRATION_PATHS: tuple[str, ...] = (
    "app/forprint_operational_registry/adapters/gateway",
    "app/forprint_operational_registry/adapters/crm",
    "app/forprint_operational_registry/adapters/telegram",
    "app/forprint_operational_registry/adapters/accounting",
    "app/forprint_operational_registry/adapters/calculator",
)

REQUIRED_V04_FILES: tuple[str, ...] = (
    "app/forprint_operational_registry/dto/errors.py",
    "app/forprint_operational_registry/dto/results.py",
    "app/forprint_operational_registry/services/operational_registry_facade.py",
    "docs/integration/public_operational_surface.md",
    "docs/integration/command_result_model.md",
    "docs/integration/reference_ready_contracts.md",
    "docs/integration/dependent_module_usage.md",
    "docs/integration/versioning_and_compatibility.md",
)

REQUIRED_MODULE_HANDOFF_EXAMPLES: tuple[str, ...] = (
    "examples/module_handoffs/telegram_bot/order_intake_draft_to_create_order.json",
    "examples/module_handoffs/crm/manual_order_create_command.json",
    "examples/module_handoffs/gateway/operational_command_envelope_create_order.json",
    "examples/module_handoffs/calculator/attach_quote_result_reference.json",
    "examples/module_handoffs/accounting/payment_reference_confirmed.json",
    "examples/module_handoffs/prepress/prepress_blocker_created.json",
)

REQUIRED_QUERY_RESULT_EXAMPLES: tuple[str, ...] = (
    "examples/query_results/order_state_for_crm.json",
    "examples/query_results/order_state_for_telegram.json",
    "examples/query_results/task_board_for_crm.json",
    "examples/query_results/order_timeline_for_operator.json",
    "examples/query_results/order_readiness_snapshot.json",
)


def load_yaml(path: Path) -> dict[str, Any]:
    """Load YAML file as dictionary."""

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")

    return data


def json_load(path: Path) -> dict[str, Any]:
    """Load JSON file as dictionary."""

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON file must contain an object: {path}")
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
    """Validate status config respects Blueprint v0.1/v0.2/v0.3 terminology."""

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
    """Validate v0.2/v0.3 did not introduce production API paths."""

    errors: list[str] = []

    for relative_path in FORBIDDEN_PRODUCTION_API_PATHS:
        if (project_root / relative_path).exists():
            errors.append(f"production API path is not approved: {relative_path}")

    return errors


def validate_checkpoint_a_files(project_root: Path) -> list[str]:
    """Validate Checkpoint A files exist."""

    errors: list[str] = []

    for relative_path in REQUIRED_CHECKPOINT_A_FILES:
        if not (project_root / relative_path).exists():
            errors.append(f"required Checkpoint A file is missing: {relative_path}")

    placeholder_dir = project_root / "app/forprint_operational_registry/contracts/placeholders"
    for filename in REQUIRED_PLACEHOLDER_CONTRACTS:
        if not (placeholder_dir / filename).exists():
            errors.append(f"required placeholder contract is missing: {filename}")

    return errors


def validate_placeholder_contracts(project_root: Path) -> list[str]:
    """Validate placeholder contracts are clearly non-canonical."""

    errors: list[str] = []
    placeholder_dir = project_root / "app/forprint_operational_registry/contracts/placeholders"

    if not placeholder_dir.exists():
        return ["placeholder contract directory is missing"]

    for filename in REQUIRED_PLACEHOLDER_CONTRACTS:
        contract_path = placeholder_dir / filename
        if not contract_path.exists():
            errors.append(f"placeholder contract is missing: {filename}")
            continue

        contract = load_yaml(contract_path)

        if contract.get("fixture_status") != "placeholder":
            errors.append(f"{filename}: fixture_status must be placeholder")

        if contract.get("canonical_contract_truth") != "forprint_library_future":
            errors.append(f"{filename}: canonical_contract_truth must point to future Library")

        if contract.get("runtime_transport_owner") != "forprint_integration_gateway_future":
            errors.append(f"{filename}: runtime_transport_owner must point to future Gateway")

        if contract.get("runtime_status") != "local_offline_fixture_only":
            errors.append(f"{filename}: runtime_status must be local_offline_fixture_only")

    return errors


def validate_foreign_import_boundary(project_root: Path) -> list[str]:
    """Validate v0.3 DTOs do not import real foreign modules."""

    errors: list[str] = []

    files_to_check = (
        project_root / "app/forprint_operational_registry/dto/envelope.py",
        project_root / "app/forprint_operational_registry/dto/references.py",
    )

    forbidden_import_tokens = (
        "forprint_integration_gateway",
        "forprint_crm",
        "telegram_bot",
        "accounting_registry",
        "calculator_engine",
        "forprint_prepress_hub",
        "forprint_library",
        "fastapi",
        "requests",
    )

    for file_path in files_to_check:
        if not file_path.exists():
            errors.append(f"foreign import boundary file is missing: {file_path}")
            continue

        import_lines = [
            line.strip().lower()
            for line in file_path.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith(("import ", "from "))
        ]

        for line in import_lines:
            for token in forbidden_import_tokens:
                if token in line:
                    errors.append(f"{file_path}: forbidden runtime import token: {token}")

    for relative_path in FORBIDDEN_REAL_INTEGRATION_PATHS:
        if (project_root / relative_path).exists():
            errors.append(f"real integration path is not approved in v0.3: {relative_path}")

    return errors


def validate_checkpoint_b_files(project_root: Path) -> list[str]:
    """Validate Checkpoint B files exist."""

    errors: list[str] = []

    for relative_path in REQUIRED_CHECKPOINT_B_FILES:
        if not (project_root / relative_path).exists():
            errors.append(f"required Checkpoint B file is missing: {relative_path}")

    return errors


def validate_blocker_config(project_root: Path) -> list[str]:
    """Validate operational blocker config."""

    errors: list[str] = []
    status_path = project_root / "app/forprint_operational_registry/config/statuses.yaml"

    if not status_path.exists():
        return ["status config is missing"]

    config = load_yaml(status_path)
    blocker_types = set(config.get("operational_blocker_types", []))
    blocker_statuses = set(config.get("operational_blocker_statuses", []))

    for blocker_type in REQUIRED_BLOCKER_TYPES:
        if blocker_type not in blocker_types:
            errors.append(f"operational blocker type is missing: {blocker_type}")

    for blocker_status in ("open", "resolved"):
        if blocker_status not in blocker_statuses:
            errors.append(f"operational blocker status is missing: {blocker_status}")

    return errors


def validate_macro_pack_files(project_root: Path) -> list[str]:
    """Validate v0.3 macro pack files exist."""

    errors: list[str] = []

    for relative_path in REQUIRED_MACRO_PACK_FILES:
        if not (project_root / relative_path).exists():
            errors.append(f"required macro pack file is missing: {relative_path}")

    return errors


def validate_handoff_fixtures(project_root: Path) -> list[str]:
    """Validate local offline handoff fixtures."""

    errors: list[str] = []
    handoff_dir = project_root / "examples/handoffs"

    for filename in REQUIRED_HANDOFF_FIXTURES:
        path = handoff_dir / filename
        if not path.exists():
            errors.append(f"handoff fixture is missing: {filename}")
            continue

        data = json_load(path)
        if data.get("fixture_status") != "example":
            errors.append(f"{filename}: fixture_status must be example")

        if data.get("runtime_transport_owner") != "forprint_integration_gateway_future":
            errors.append(f"{filename}: runtime_transport_owner must point to future Gateway")

        if data.get("canonical_contract_truth") != "forprint_library_future":
            errors.append(f"{filename}: canonical_contract_truth must point to future Library")

    return errors


def validate_projection_fixtures(project_root: Path) -> list[str]:
    """Validate projection example fixtures."""

    errors: list[str] = []
    projection_dir = project_root / "examples/projections"

    for filename in REQUIRED_PROJECTION_FIXTURES:
        path = projection_dir / filename
        if not path.exists():
            errors.append(f"projection fixture is missing: {filename}")
            continue

        data = json_load(path)
        if data.get("fixture_status") != "example":
            errors.append(f"{filename}: fixture_status must be example")

    return errors


def validate_v04_files(project_root: Path) -> list[str]:
    """Validate v0.4 reference-ready integration surface files."""

    errors: list[str] = []

    for relative_path in REQUIRED_V04_FILES:
        if not (project_root / relative_path).exists():
            errors.append(f"required v0.4 file is missing: {relative_path}")

    return errors


def validate_module_handoff_examples(project_root: Path) -> list[str]:
    """Validate module handoff examples."""

    errors: list[str] = []

    for relative_path in REQUIRED_MODULE_HANDOFF_EXAMPLES:
        path = project_root / relative_path
        if not path.exists():
            errors.append(f"module handoff example is missing: {relative_path}")
            continue

        data = json_load(path)
        if data.get("fixture_status") != "example":
            errors.append(f"{relative_path}: fixture_status must be example")

        if data.get("real_integration") is not False:
            errors.append(f"{relative_path}: real_integration must be false")

        if data.get("transport_owner_future") != "forprint_integration_gateway":
            errors.append(f"{relative_path}: transport owner must be future Gateway")

        if data.get("canonical_contract_truth_future") != "forprint_library":
            errors.append(f"{relative_path}: canonical truth must be future Library")

        if "schema_version" not in data:
            errors.append(f"{relative_path}: schema_version is missing")

        if "contract_version" not in data:
            errors.append(f"{relative_path}: contract_version is missing")

    return errors


def validate_query_result_examples(project_root: Path) -> list[str]:
    """Validate query/projection result examples."""

    errors: list[str] = []

    for relative_path in REQUIRED_QUERY_RESULT_EXAMPLES:
        path = project_root / relative_path
        if not path.exists():
            errors.append(f"query result example is missing: {relative_path}")
            continue

        data = json_load(path)
        if data.get("fixture_status") != "example":
            errors.append(f"{relative_path}: fixture_status must be example")

        if "schema_version" not in data:
            errors.append(f"{relative_path}: schema_version is missing")

        payload = data.get("payload", {})
        forbidden = {"payment_truth", "invoice_truth", "product_catalog", "material_catalog"}
        if isinstance(payload, dict) and forbidden.intersection(payload):
            errors.append(f"{relative_path}: contains forbidden foreign truth fields")

    return errors
