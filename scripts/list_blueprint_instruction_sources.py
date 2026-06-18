from pathlib import Path

import yaml

BLUEPRINT_ROOT = Path("/srv/software_development/forprint-project/forprint_system_blueprint")
SOURCES_PATH = BLUEPRINT_ROOT / "coordination/instruction_intake/instruction_sources.yaml"


def main() -> int:
    print("== Operational Registry Blueprint instruction sources ==")
    data = yaml.safe_load(SOURCES_PATH.read_text(encoding="utf-8"))
    print(f"Instruction intake: {SOURCES_PATH}")
    for item in data.get("priority_order", []):
        priority = item.get("priority")
        source_id = item.get("source_id")
        behavior = item.get("behavior")
        title = item.get("title")
        print(f"- {priority:>2} {source_id}: {behavior} — {title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
