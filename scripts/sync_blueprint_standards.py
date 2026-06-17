from __future__ import annotations

import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

MODULE_ID = "forprint_operational_registry"
BLUEPRINT_ROOT = Path("/srv/software_development/forprint-project/forprint_system_blueprint")
STANDARDS_INDEX = BLUEPRINT_ROOT / "coordination/standards/index.yaml"
OUTPUT_PATH = Path("coordination/standards/blueprint_standards_snapshot.yaml")


def blueprint_commit() -> str:
    result = subprocess.run(
        ["git", "-C", str(BLUEPRINT_ROOT), "rev-parse", "--short", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def find_advisory_semantics(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        if value.get("standards_are_advisory_by_default") is True:
            return value
        if value.get("advisory_by_default") is True:
            return {
                "standards_are_advisory_by_default": True,
                "source_key": "advisory_by_default",
            }
        for item in value.values():
            found = find_advisory_semantics(item)
            if found:
                return found

    if isinstance(value, list):
        for item in value:
            found = find_advisory_semantics(item)
            if found:
                return found

    return {}


def fallback_advisory_semantics(raw_text: str) -> dict[str, Any]:
    lowered = raw_text.lower()
    if "advisory" in lowered and (
        "default" in lowered
        or "by_default" in lowered
        or "unless activated" in lowered
        or "unless explicitly" in lowered
    ):
        return {
            "standards_are_advisory_by_default": True,
            "source": "standards_index_text",
        }
    return {}


def main() -> int:
    raw_text = STANDARDS_INDEX.read_text(encoding="utf-8")
    index = yaml.safe_load(raw_text)
    standards = index.get("standards", [])
    advisory_semantics = find_advisory_semantics(index) or fallback_advisory_semantics(raw_text)

    snapshot = {
        "snapshot_id": "operational_registry_blueprint_standards_snapshot_v0_1",
        "module_id": MODULE_ID,
        "source_blueprint_path": str(BLUEPRINT_ROOT),
        "source_blueprint_commit": blueprint_commit(),
        "snapshot_timestamp": datetime.now(UTC).isoformat(),
        "standards_index_path": "coordination/standards/index.yaml",
        "standards_index_version": index.get("standards_index_version"),
        "standards_count": len(standards),
        "reviewed_standards": standards,
        "required_reviewed_standards": [
            "coordination/standards/index.yaml",
            "coordination/standards/module_standards_awareness_protocol.md",
            "coordination/standards/module_governance_protocol.md",
            "coordination/standards/module_make_target_contract.md",
        ],
        "advisory_semantics_confirmation": advisory_semantics,
        "operational_registry_alignment_notes": [
            "Operational Registry reads Blueprint standards without taking foreign ownership.",
            "Standards remain advisory unless activated by prompt/directive.",
            "No production API, live write, final pricing, accounting truth "
            "or Library catalog ownership was added.",
        ],
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(yaml.safe_dump(snapshot, sort_keys=False), encoding="utf-8")
    print("✅ Operational Registry Blueprint standards snapshot refreshed.")
    print(f"  - {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())