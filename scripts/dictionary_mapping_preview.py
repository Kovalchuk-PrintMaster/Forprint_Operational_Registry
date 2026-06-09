"""Render dictionary mapping preview."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from forprint_operational_registry.services.dictionary_mapping import (  # noqa: E402
    build_dictionary_alignment_result,
    build_dictionary_version_pin,
    detect_deprecated_library_references,
    detect_unmapped_local_values,
    load_local_dictionary_mapping,
    resolve_local_value_to_library,
)

from scripts.client_card_preview import key_value_table, render_table  # noqa: E402


def render_dictionary_mapping_preview() -> str:
    """Render dictionary mapping preview."""

    data = load_local_dictionary_mapping()
    pin = build_dictionary_version_pin(data)
    result = build_dictionary_alignment_result(data)
    unresolved = detect_unmapped_local_values(data)
    deprecated = detect_deprecated_library_references(data)

    sample_confirmed = [
        resolve_local_value_to_library("order_status", "needs_review", data),
        resolve_local_value_to_library("workflow_stage_status", "in_progress", data),
        resolve_local_value_to_library("payment_status", "partially_paid", data),
        resolve_local_value_to_library("material_requirement_status", "planned", data),
        resolve_local_value_to_library("alert_event_status", "open", data),
        resolve_local_value_to_library("unit", "pcs", data),
    ]

    manual_review = [
        resolve_local_value_to_library(
            "product_service_reference_status",
            "ambiguous_manual_review_required",
            data,
        )
    ]

    return "\n\n".join(
        [
            "ForPrint Operational Registry — Dictionary Mapping Preview",
            key_value_table(
                "DICTIONARY VERSION PIN",
                {
                    "dictionary_version_pin_id": pin.dictionary_version_pin_id,
                    "library_dictionary_version": pin.library_dictionary_version,
                    "library_commit_ref": pin.library_commit_ref,
                    "status": pin.status,
                },
                [
                    "dictionary_version_pin_id",
                    "library_dictionary_version",
                    "library_commit_ref",
                    "status",
                ],
            ),
            render_table(
                "MAPPED GROUPS",
                ["group"],
                [[group] for group in result.groups_checked],
            ),
            render_table(
                "CONFIRMED MAPPINGS",
                ["group", "local", "canonical", "status"],
                [
                    [
                        item.local_group,
                        item.local_value,
                        item.library_canonical_id,
                        item.mapping_status,
                    ]
                    for item in sample_confirmed
                ],
            ),
            render_table(
                "UNRESOLVED VALUES",
                ["group", "local", "status"],
                [[item.local_group, item.local_value, item.mapping_status] for item in unresolved]
                or [["none", "none", "none"]],
            ),
            render_table(
                "DEPRECATED REFERENCES",
                ["group", "local", "canonical", "status"],
                [
                    [
                        item.local_group,
                        item.local_value,
                        item.library_canonical_id,
                        item.mapping_status,
                    ]
                    for item in deprecated
                ]
                or [["none", "none", "none", "none"]],
            ),
            render_table(
                "MANUAL REVIEW REQUIRED",
                ["group", "local", "canonical", "status"],
                [
                    [
                        item.local_group,
                        item.local_value,
                        item.library_canonical_id,
                        item.mapping_status,
                    ]
                    for item in manual_review
                ],
            ),
            key_value_table(
                "ALIGNMENT SUMMARY",
                {
                    "confirmed_count": result.confirmed_count,
                    "unresolved_count": result.unresolved_count,
                    "deprecated_count": result.deprecated_count,
                    "manual_review_count": result.manual_review_count,
                    "warnings": ", ".join(result.warnings),
                },
                [
                    "confirmed_count",
                    "unresolved_count",
                    "deprecated_count",
                    "manual_review_count",
                    "warnings",
                ],
            ),
        ]
    )


def main() -> int:
    """CLI entrypoint."""

    print(render_dictionary_mapping_preview())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
