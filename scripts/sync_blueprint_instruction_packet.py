from __future__ import annotations

import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

MODULE_ID = "forprint_operational_registry"
MODULE_PROFILE = {
    "maturity": "active_development",
    "business_criticality": "core",
    "complexity": "high",
    "automation_level": "medium",
    "standards_strictness": "growing",
    "prompt_priority": "high",
    "cleanup_priority": "medium",
    "feedback_required": True,
}
BLUEPRINT_ROOT = Path("/srv/software_development/forprint-project/forprint_system_blueprint")
SOURCES_PATH = BLUEPRINT_ROOT / "coordination/instruction_intake/instruction_sources.yaml"
OUTPUT_PATH = Path("coordination/instruction_intake/blueprint_instruction_packet.yaml")

VOLATILE_SNAPSHOT_KEYS: frozenset[str] = frozenset(
    {
        "generated_at",
        "snapshot_created_at",
        "snapshot_timestamp",
        "last_synced_at",
        "synced_at",
        "refreshed_at",
        "updated_at",
    }
)


def blueprint_commit() -> str:
    result = subprocess.run(
        ["git", "-C", str(BLUEPRINT_ROOT), "rev-parse", "--short", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def semantic_payload(value: Any) -> Any:
    """Return payload without volatile timestamp-only fields."""

    if isinstance(value, dict):
        return {
            key: semantic_payload(item)
            for key, item in value.items()
            if key not in VOLATILE_SNAPSHOT_KEYS
        }

    if isinstance(value, list):
        return [semantic_payload(item) for item in value]

    return value


def yaml_payload(path: Path) -> dict[str, Any] | None:
    """Load YAML mapping from path if it exists."""

    if not path.exists():
        return None

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return None

    return data


def write_yaml_if_semantic_changed(payload: dict[str, Any], path: Path) -> bool:
    """Write YAML only if semantic payload changed.

    Returns True when file was written.
    """

    existing = yaml_payload(path)
    if existing is not None:
        if semantic_payload(existing) == semantic_payload(payload):
            return False

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return True


def build_instruction_packet() -> dict[str, Any]:
    """Build local Blueprint instruction packet snapshot."""

    sources = yaml.safe_load(SOURCES_PATH.read_text(encoding="utf-8"))
    if not isinstance(sources, dict):
        raise ValueError("Blueprint instruction sources must be a YAML mapping")

    return {
        "packet_id": "operational_registry_blueprint_instruction_packet_v0_1",
        "module_id": MODULE_ID,
        "source_blueprint_path": str(BLUEPRINT_ROOT),
        "source_blueprint_commit": blueprint_commit(),
        "generated_at": datetime.now(UTC).isoformat(),
        "instruction_intake_version": sources.get("instruction_intake_version"),
        "priority_order_confirmed": True,
        "freshness_policy_confirmed": True,
        "module_profile": MODULE_PROFILE,
        "instruction_sources_reviewed": [
            "coordination/instruction_intake/assistant_reading_order.md",
            "coordination/instruction_intake/instruction_sources.yaml",
            "coordination/instruction_intake/module_profile_model.md",
            "coordination/instruction_intake/default_profile_traits.yaml",
        ],
        "boundary_confirmation": {
            "no_production_api_added": True,
            "no_live_write_added": True,
            "no_real_external_integrations_added": True,
            "no_accounting_truth_added": True,
            "no_library_catalog_ownership_added": True,
            "no_crm_dashboard_added": True,
            "no_final_price_calculation_added": True,
        },
        "questions_for_blueprint": [],
    }


def main() -> int:
    packet = build_instruction_packet()
    changed = write_yaml_if_semantic_changed(packet, OUTPUT_PATH)

    if changed:
        print("✅ Operational Registry Blueprint instruction packet refreshed.")
    else:
        print("✅ Operational Registry Blueprint instruction packet already up to date.")
    print(f"  - {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
