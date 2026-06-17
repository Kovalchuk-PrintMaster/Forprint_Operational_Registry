from pathlib import Path

import yaml

BLUEPRINT_ROOT = Path("/srv/software_development/forprint-project/forprint_system_blueprint")
STANDARDS_INDEX = BLUEPRINT_ROOT / "coordination/standards/index.yaml"


def main() -> int:
    print("== Operational Registry Blueprint standards list ==")
    data = yaml.safe_load(STANDARDS_INDEX.read_text(encoding='utf-8'))
    standards = data.get('standards', [])
    print(f"Standards index: {STANDARDS_INDEX}")
    print(f"Standards count: {len(standards)}")
    for standard in standards:
        standard_id = standard.get('standard_id')
        file_path = standard.get('file')
        status = standard.get('status')
        adoption_mode = standard.get('adoption_mode')
        print(f"- {standard_id}: {file_path} [{status}, {adoption_mode}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
