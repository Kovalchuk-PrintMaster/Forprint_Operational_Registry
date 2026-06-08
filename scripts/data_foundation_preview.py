"""Render ForPrint data foundation preview in terminal."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.client_card_preview import key_value_table, render_table  # noqa: E402

EXAMPLES_DIR = PROJECT_ROOT / "examples/data_foundation"


def load_yaml(path: Path) -> dict[str, Any]:
    """Load YAML file."""

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping: {path}")
    return data


def render_data_foundation_preview() -> str:
    """Render data foundation preview."""

    master = load_yaml(EXAMPLES_DIR / "master_data_record.example.yaml")
    fact = load_yaml(EXAMPLES_DIR / "operational_fact_record.example.yaml")
    event = load_yaml(EXAMPLES_DIR / "operational_event_record.example.yaml")
    external = load_yaml(EXAMPLES_DIR / "external_reference.example.yaml")
    report = load_yaml(EXAMPLES_DIR / "report_definition.example.yaml")
    projection = load_yaml(EXAMPLES_DIR / "data_projection.example.yaml")

    sections = [
        "ForPrint Operational Registry — Data Foundation Preview",
        "",
        key_value_table(
            "MASTER DATA BASE RECORD",
            master["record"],
            [
                "internal_id",
                "entity_type",
                "display_name",
                "canonical_name",
                "source_system",
                "raw_source_name",
            ],
        ),
        "",
        key_value_table(
            "OPERATIONAL FACT RECORD",
            fact["record"],
            [
                "fact_id",
                "fact_type",
                "business_date",
                "client_account_id",
                "source_system",
                "source_ref",
                "status",
            ],
        ),
        "",
        key_value_table(
            "EVENT RECORD",
            event["record"],
            [
                "event_id",
                "event_type",
                "target_entity_type",
                "target_entity_id",
                "source_system",
                "actor_ref",
            ],
        ),
        "",
        key_value_table(
            "EXTERNAL REFERENCES",
            external["record"],
            [
                "external_reference_id",
                "internal_entity_type",
                "internal_entity_id",
                "external_system",
                "external_entity_type",
                "external_code",
                "external_ref",
            ],
        ),
        "",
        key_value_table(
            "REPORT DEFINITION",
            report["record"],
            [
                "report_definition_id",
                "report_name",
                "report_type",
                "default_period",
                "status",
            ],
        ),
        "",
        render_table(
            "DATA PROJECTION",
            ["projection_id", "type", "dimensions", "metrics", "rows"],
            [
                [
                    projection["record"]["projection_id"],
                    projection["record"]["projection_type"],
                    ", ".join(projection["record"]["dimensions"]),
                    ", ".join(projection["record"]["metrics"]),
                    len(projection["record"]["rows"]),
                ]
            ],
        ),
        "",
        render_table(
            "EXAMPLE REPORT QUESTIONS",
            ["question"],
            [[question] for question in projection["example_report_questions"]],
        ),
    ]

    return "\n".join(sections)


def main() -> int:
    """CLI entrypoint."""

    print(render_data_foundation_preview())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
