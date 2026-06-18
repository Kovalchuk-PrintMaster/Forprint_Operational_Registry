from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

BLUEPRINT_ROOT = Path("/srv/software_development/forprint-project/forprint_system_blueprint")
STANDARDS_ROOT = BLUEPRINT_ROOT / "coordination/standards"
STANDARDS_INDEX = STANDARDS_ROOT / "index.yaml"
SNAPSHOT_PATH = Path("coordination/standards/blueprint_standards_snapshot.yaml")


def has_explicit_advisory_semantics(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key).lower()
            if (
                key_text
                in {
                    "standards_are_advisory_by_default",
                    "advisory_by_default",
                    "standards_advisory_by_default",
                }
                and item is True
            ):
                return True
            if has_explicit_advisory_semantics(item):
                return True

    if isinstance(value, list):
        return any(has_explicit_advisory_semantics(item) for item in value)

    return False


def raw_text_has_advisory_semantics(text: str) -> bool:
    lowered = text.lower()
    return "advisory" in lowered and (
        "default" in lowered
        or "by_default" in lowered
        or "unless activated" in lowered
        or "unless explicitly" in lowered
    )


def main() -> int:
    print("== Operational Registry Blueprint standards visibility check ==")
    issues: list[str] = []

    if not STANDARDS_INDEX.is_file():
        issues.append(f"Standards index does not exist: {STANDARDS_INDEX}")
        data: dict[str, Any] = {}
        raw_text = ""
    else:
        raw_text = STANDARDS_INDEX.read_text(encoding="utf-8")
        data = yaml.safe_load(raw_text) or {}

    standards = data.get("standards")
    if not isinstance(standards, list) or not standards:
        issues.append("standards index must contain non-empty standards list")
    else:
        for standard in standards:
            file_name = standard.get("file") if isinstance(standard, dict) else None
            if isinstance(file_name, str) and file_name:
                standard_path = STANDARDS_ROOT / file_name
                if not standard_path.is_file():
                    issues.append(f"missing standards file: {standard_path}")

    if not (has_explicit_advisory_semantics(data) or raw_text_has_advisory_semantics(raw_text)):
        issues.append("standards advisory semantics must be explicit")

    if SNAPSHOT_PATH.is_file():
        snapshot = yaml.safe_load(SNAPSHOT_PATH.read_text(encoding="utf-8")) or {}
        if snapshot.get("module_id") != "forprint_operational_registry":
            issues.append("local standards snapshot module_id is invalid")
        if isinstance(standards, list) and snapshot.get("standards_count") != len(standards):
            issues.append("local standards snapshot standards_count is stale")

    if issues:
        print("❌ Blueprint standards visibility check failed:")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("✅ Blueprint standards index readable")
    print("✅ Advisory semantics explicit")
    print("✅ Operational Registry standards visibility is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
