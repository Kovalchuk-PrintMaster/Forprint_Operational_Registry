"""Export local module status for future Project Inspector readiness."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = PROJECT_ROOT / "reports/operational_registry_module_status.json"


def load_yaml(path: Path) -> dict[str, Any]:
    """Load YAML file."""

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in YAML file: {path}")
    return data


def build_module_status() -> dict[str, Any]:
    """Build module status payload."""

    manifest = load_yaml(PROJECT_ROOT / "forprint_module_manifest.yaml")

    return {
        "module_id": manifest["module_id"],
        "module_status": manifest.get("status", "unknown"),
        "version": manifest.get("version"),
        "public_surface_status": "reference_ready_internal_offline",
        "facade_status": "internal_adapter_facing_facade_available",
        "implemented_layers": [
            "domain_models",
            "command_query_dtos",
            "command_result_dtos",
            "error_warning_taxonomy",
            "repository_interfaces",
            "in_memory_repositories",
            "service_layer",
            "facade_layer",
            "lifecycle_validation",
            "operational_blockers",
            "operational_projections",
            "handoff_fixtures",
            "module_status_export",
        ],
        "command_dtos": [
            "CreateClientCommand",
            "CreateOrderCommand",
            "ChangeOrderStatusCommand",
            "CreateOperationalTaskCommand",
            "AssignOperationalTaskCommand",
            "ChangeTaskStatusCommand",
            "AddOperationalNoteCommand",
            "AppendOperationalEventCommand",
        ],
        "query_dtos": [
            "GetOrderByIdQuery",
            "ListOrdersByClientQuery",
            "ListTasksByOrderQuery",
            "GetOrderStateQuery",
            "GetOrderHistoryQuery",
            "ListOrdersByStatusQuery",
        ],
        "projection_dtos": [
            "OrderStateProjection",
            "OrderListItemProjection",
            "ClientOperationalSummary",
            "TaskBoardProjection",
            "OperationalTimelineProjection",
            "OperationalReadinessSnapshot",
            "OperationalHealthSnapshot",
        ],
        "owned_objects": manifest.get("owns", []),
        "must_not_own": manifest.get("must_not_own", []),
        "examples_status": {
            "module_handoffs": "examples/module_handoffs",
            "query_results": "examples/query_results",
            "legacy_handoff_examples": "examples/handoffs",
            "projection_examples": "examples/projections",
        },
        "check_summary": {
            "local_check_report": "reports/operational_registry_check_report.json",
            "module_status_report": str(REPORT_PATH),
        },
        "open_questions": [
            "When should production API be introduced?",
            "When should persistent storage strategy be selected?",
            "Which contracts should ForPrint Library canonicalize first?",
            "Which Gateway/CRM adapter should be prototyped first after approval?",
        ],
        "boundary_marker": {
            "no_production_api": True,
            "no_real_integrations": True,
            "no_database_migrations": True,
            "no_foreign_runtime_data": True,
            "no_foreign_domain_ownership": True,
        },
        "generated_at": datetime.now(UTC).isoformat(),
        "last_generated_at": datetime.now(UTC).isoformat(),
    }


def export_module_status() -> Path:
    """Write module status JSON report."""

    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(build_module_status(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return REPORT_PATH


def main() -> int:
    """CLI entrypoint."""

    path = export_module_status()
    print(f"📄 Module status report: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
