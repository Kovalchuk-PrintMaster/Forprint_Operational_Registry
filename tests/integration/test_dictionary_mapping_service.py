from forprint_operational_registry.services.dictionary_mapping import (
    REQUIRED_MAPPING_GROUPS,
    build_dictionary_alignment_result,
    build_dictionary_version_pin,
    detect_deprecated_library_references,
    detect_unmapped_local_values,
    load_local_dictionary_mapping,
    resolve_local_value_to_library,
    validate_local_dictionary_mapping,
)


def test_mapping_config_loads_and_required_groups_exist() -> None:
    data = load_local_dictionary_mapping()
    errors = validate_local_dictionary_mapping(data)

    assert errors == []
    assert set(REQUIRED_MAPPING_GROUPS).issubset(set(data["mappings"]))


def test_known_order_status_maps_to_library_canonical_id() -> None:
    mapping = resolve_local_value_to_library("order_status", "needs_review")

    assert mapping.mapping_status == "confirmed"
    assert mapping.library_canonical_id == "order_status.needs_review"


def test_known_workflow_stage_status_maps_to_library_canonical_id() -> None:
    mapping = resolve_local_value_to_library("workflow_stage_status", "in_progress")

    assert mapping.mapping_status == "confirmed"
    assert mapping.library_canonical_id == "workflow_stage_status.in_progress"


def test_known_payment_status_maps_to_library_canonical_id() -> None:
    mapping = resolve_local_value_to_library("payment_status", "partially_paid")

    assert mapping.mapping_status == "confirmed"
    assert mapping.library_canonical_id == "payment_status.partially_paid"


def test_known_material_requirement_status_maps_to_library_canonical_id() -> None:
    mapping = resolve_local_value_to_library(
        "material_requirement_status",
        "warehouse_reference_pending",
    )

    assert mapping.mapping_status == "confirmed"
    assert mapping.library_canonical_id == (
        "material_requirement_status.warehouse_reference_pending"
    )


def test_known_alert_values_map_to_library_canonical_ids() -> None:
    severity = resolve_local_value_to_library("alert_severity", "warning")
    event_status = resolve_local_value_to_library("alert_event_status", "open")

    assert severity.library_canonical_id == "alert_severity.warning"
    assert event_status.library_canonical_id == "alert_event_status.open"


def test_unit_values_map_to_library_canonical_ids() -> None:
    mapping = resolve_local_value_to_library("unit", "m2")

    assert mapping.mapping_status == "confirmed"
    assert mapping.library_canonical_id == "unit.m2"


def test_unknown_local_value_returns_unresolved() -> None:
    mapping = resolve_local_value_to_library("order_status", "strange_new_status")

    assert mapping.mapping_status == "unresolved"


def test_deprecated_canonical_reference_is_detected() -> None:
    deprecated = detect_deprecated_library_references()

    assert any(item.local_value == "paid" for item in deprecated)


def test_no_unmapped_local_values_for_known_groups() -> None:
    assert detect_unmapped_local_values() == []


def test_dictionary_version_pin_and_alignment_result() -> None:
    data = load_local_dictionary_mapping()
    pin = build_dictionary_version_pin(data)
    result = build_dictionary_alignment_result(data)

    assert pin.library_dictionary_version == "shared_operational_dictionary_v0_1"
    assert result.confirmed_count > 0
    assert result.unresolved_count == 0
