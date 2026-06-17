import subprocess
from datetime import UTC, datetime
from pathlib import Path

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


def blueprint_commit() -> str:
    result = subprocess.run(
        ["git", "-C", str(BLUEPRINT_ROOT), "rev-parse", "--short", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def main() -> int:
    sources = yaml.safe_load(SOURCES_PATH.read_text(encoding='utf-8'))
    packet = {
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
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(yaml.safe_dump(packet, sort_keys=False), encoding='utf-8')
    print("✅ Operational Registry Blueprint instruction packet refreshed.")
    print(f"  - {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
