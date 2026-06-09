"""Dictionary mapping helpers.

No runtime Library dependency is required here.
Operational Registry only validates local values against a local mapping config.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any
from uuid import uuid4

import yaml

from forprint_operational_registry.models.dictionary_mapping import (
    DictionaryAlignmentResult,
    DictionaryVersionPin,
    LocalEnumMapping,
    utc_now,
)
from forprint_operational_registry.models.order_workflow import (
    ALERT_EVENT_STATUSES,
    ALERT_NOTIFICATION_STATUSES,
    ALERT_RULE_TYPES,
    ALERT_SEVERITIES,
    CONTRACTOR_RESOLUTION_STATUSES,
    DEADLINE_TYPES,
    MATERIAL_REQUIREMENT_STATUSES,
    ORDER_STATUSES,
    PAYMENT_VISIBILITY_STATUSES,
    PRODUCT_SERVICE_RESOLUTION_STATUSES,
    PRODUCTION_STATUSES,
    WORKFLOW_STATUSES,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MAPPING_PATH = (
    PROJECT_ROOT / "config/dictionary_mapping/operational_registry_to_library_v0_1.yaml"
)

REQUIRED_MAPPING_GROUPS: tuple[str, ...] = (
    "source_system",
    "entity_type",
    "order_status",
    "order_line_status",
    "payment_status",
    "production_status",
    "workflow_status",
    "workflow_stage_status",
    "material_requirement_status",
    "reference_resolution_status",
    "product_service_reference_status",
    "contractor_reference_status",
    "deadline_type",
    "alert_rule_type",
    "alert_severity",
    "alert_event_status",
    "notification_status",
    "unit",
)

LOCAL_ENUM_VALUES: dict[str, tuple[str, ...]] = {
    "source_system": (
        "manual",
        "sanitized_demo",
        "calculator_engine",
        "1c_bas",
        "telegram_bot_legacy",
        "unknown",
    ),
    "entity_type": (
        "client_account",
        "order",
        "order_line",
        "workflow_stage",
        "payment_projection",
        "material_requirement",
        "alert_rule",
        "alert_event",
        "external_reference",
        "report_projection",
        "unknown",
    ),
    "order_status": ORDER_STATUSES,
    "order_line_status": ORDER_STATUSES,
    "payment_status": PAYMENT_VISIBILITY_STATUSES,
    "production_status": PRODUCTION_STATUSES,
    "workflow_status": WORKFLOW_STATUSES,
    "workflow_stage_status": WORKFLOW_STATUSES,
    "material_requirement_status": MATERIAL_REQUIREMENT_STATUSES,
    "reference_resolution_status": PRODUCT_SERVICE_RESOLUTION_STATUSES,
    "product_service_reference_status": PRODUCT_SERVICE_RESOLUTION_STATUSES,
    "contractor_reference_status": CONTRACTOR_RESOLUTION_STATUSES,
    "deadline_type": DEADLINE_TYPES,
    "alert_rule_type": ALERT_RULE_TYPES,
    "alert_severity": ALERT_SEVERITIES,
    "alert_event_status": ALERT_EVENT_STATUSES,
    "notification_status": ALERT_NOTIFICATION_STATUSES,
    "unit": ("pcs", "m2", "m", "kg", "liter", "hour", "unknown"),
}


def load_local_dictionary_mapping(path: Path = DEFAULT_MAPPING_PATH) -> dict[str, Any]:
    """Load local dictionary mapping YAML."""

    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValueError("Dictionary mapping config must be a YAML mapping")

    return data


def get_mapping_entries(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Return mapping entries by group."""

    mappings = data.get("mappings")
    if not isinstance(mappings, dict):
        raise ValueError("Dictionary mapping config must contain mappings")

    return mappings


def validate_local_dictionary_mapping(data: dict[str, Any]) -> list[str]:
    """Validate local dictionary mapping config."""

    errors: list[str] = []
    mappings = get_mapping_entries(data)

    if data.get("library_authority") != "forprint_library":
        errors.append("library_authority must be forprint_library")

    if data.get("runtime_library_dependency") is not False:
        errors.append("runtime_library_dependency must be false")

    if data.get("operational_registry_edits_library") is not False:
        errors.append("operational_registry_edits_library must be false")

    for group in REQUIRED_MAPPING_GROUPS:
        if group not in mappings:
            errors.append(f"required mapping group is missing: {group}")
            continue

        group_mapping = mappings[group]
        if not isinstance(group_mapping, dict):
            errors.append(f"mapping group must be a mapping: {group}")

    return errors


def build_local_enum_mapping(
    group: str,
    local_value: str,
    entry: dict[str, Any] | None,
) -> LocalEnumMapping:
    """Build LocalEnumMapping from YAML entry."""

    if entry is None:
        return LocalEnumMapping(
            mapping_id=f"map_{group}_{local_value}",
            local_group=group,
            local_value=local_value,
            library_dictionary_group=group,
            mapping_status="unresolved",
            notes="Local value is not mapped.",
        )

    canonical_id = entry.get("canonical_id")
    mapping_status = entry.get("status", "unknown")

    return LocalEnumMapping(
        mapping_id=f"map_{group}_{local_value}",
        local_group=group,
        local_value=local_value,
        library_dictionary_group=group,
        library_canonical_id=canonical_id,
        mapping_status=mapping_status,
        resolution_source=entry.get("resolution_source", "local_mapping_config"),
        notes=entry.get("notes"),
    )


def resolve_local_value_to_library(
    group: str,
    local_value: str,
    data: dict[str, Any] | None = None,
) -> LocalEnumMapping:
    """Resolve local enum value to Library canonical dictionary ID."""

    mapping_data = data or load_local_dictionary_mapping()
    mappings = get_mapping_entries(mapping_data)
    entry = mappings.get(group, {}).get(local_value)

    return build_local_enum_mapping(group, local_value, entry)


def detect_unmapped_local_values(data: dict[str, Any] | None = None) -> list[LocalEnumMapping]:
    """Detect local values missing from mapping config."""

    mapping_data = data or load_local_dictionary_mapping()
    mappings = get_mapping_entries(mapping_data)
    unresolved: list[LocalEnumMapping] = []

    for group, local_values in LOCAL_ENUM_VALUES.items():
        group_mapping = mappings.get(group, {})
        for local_value in local_values:
            if local_value not in group_mapping:
                unresolved.append(build_local_enum_mapping(group, local_value, None))

    return unresolved


def detect_deprecated_library_references(
    data: dict[str, Any] | None = None,
) -> list[LocalEnumMapping]:
    """Detect mapping entries marked as deprecated references."""

    mapping_data = data or load_local_dictionary_mapping()
    mappings = get_mapping_entries(mapping_data)
    deprecated: list[LocalEnumMapping] = []

    for group, group_mapping in mappings.items():
        for local_value, entry in group_mapping.items():
            if entry.get("status") == "deprecated_reference":
                deprecated.append(build_local_enum_mapping(group, local_value, entry))

    return deprecated


def build_dictionary_version_pin(data: dict[str, Any]) -> DictionaryVersionPin:
    """Build DictionaryVersionPin from config."""

    pin = data.get("dictionary_version_pin")
    if not isinstance(pin, dict):
        raise ValueError("dictionary_version_pin is required")

    return DictionaryVersionPin(
        dictionary_version_pin_id=pin["dictionary_version_pin_id"],
        library_dictionary_version=pin["library_dictionary_version"],
        library_commit_ref=pin.get("library_commit_ref"),
        status=pin.get("status", "active"),
        notes=pin.get("notes"),
    )


def build_dictionary_alignment_result(
    data: dict[str, Any] | None = None,
) -> DictionaryAlignmentResult:
    """Build alignment result summary."""

    mapping_data = data or load_local_dictionary_mapping()
    mappings = get_mapping_entries(mapping_data)

    statuses = Counter()
    for group_mapping in mappings.values():
        for entry in group_mapping.values():
            statuses[entry.get("status", "unknown")] += 1

    unresolved_count = len(detect_unmapped_local_values(mapping_data))
    warnings = []

    if unresolved_count:
        warnings.append(f"Unmapped local values detected: {unresolved_count}")

    return DictionaryAlignmentResult(
        alignment_result_id=f"dict_alignment_{uuid4().hex}",
        checked_at=utc_now(),
        groups_checked=tuple(sorted(mappings)),
        confirmed_count=statuses["confirmed"] + statuses["confirmed_with_alias"],
        unresolved_count=unresolved_count + statuses["unresolved"],
        deprecated_count=statuses["deprecated_reference"],
        manual_review_count=statuses["manual_review_required"],
        warnings=tuple(warnings),
    )
