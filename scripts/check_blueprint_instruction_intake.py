import subprocess
from pathlib import Path

import yaml

MODULE_ID = "forprint_operational_registry"
BLUEPRINT_ROOT = Path("/srv/software_development/forprint-project/forprint_system_blueprint")
SOURCES_PATH = BLUEPRINT_ROOT / "coordination/instruction_intake/instruction_sources.yaml"
READING_ORDER_PATH = BLUEPRINT_ROOT / "coordination/instruction_intake/assistant_reading_order.md"


REQUIRED_PRIORITY_IDS = [
    "instruction_intake",
    "global_policy",
    "active_directives",
    "module_policy",
    "outgoing_prompt",
    "standards",
    "current_status_and_reports",
    "local_implementation",
]


def blueprint_commit() -> str:
    result = subprocess.run(
        ["git", "-C", str(BLUEPRINT_ROOT), "rev-parse", "--short", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def main() -> int:
    print("== Operational Registry Blueprint instruction intake check ==")
    issues: list[str] = []

    if not BLUEPRINT_ROOT.exists():
        issues.append(f"Blueprint root does not exist: {BLUEPRINT_ROOT}")
    if not SOURCES_PATH.is_file():
        issues.append(f"Instruction sources file does not exist: {SOURCES_PATH}")
    if not READING_ORDER_PATH.is_file():
        issues.append(f"Reading order file does not exist: {READING_ORDER_PATH}")

    data = {}
    if SOURCES_PATH.is_file():
        data = yaml.safe_load(SOURCES_PATH.read_text(encoding='utf-8')) or {}
        if data.get('status') != 'active':
            issues.append("instruction_sources.yaml status must be active")
        freshness = data.get('freshness_policy') or {}
        if freshness.get('read_blueprint_source_on_each_prompt') is not True:
            issues.append("freshness policy must require reading Blueprint source on each prompt")
        priority_ids = [item.get('source_id') for item in data.get('priority_order', [])]
        for source_id in REQUIRED_PRIORITY_IDS:
            if source_id not in priority_ids:
                issues.append(f"missing priority source_id: {source_id}")

    if issues:
        print("❌ Blueprint instruction intake check failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print(f"✅ Blueprint instruction intake is readable for {MODULE_ID}")
    print(f"✅ Blueprint commit: {blueprint_commit()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
