import pytest
from forprint_operational_registry.models.dictionary_mapping import (
    CanonicalDictionaryReference,
    DictionaryVersionPin,
    LocalEnumMapping,
)


def test_canonical_dictionary_reference_can_be_created() -> None:
    reference = CanonicalDictionaryReference(
        dictionary_reference_id="dict_ref_order_status_new",
        dictionary_group="order_status",
        canonical_id="order_status.new",
        library_version="shared_operational_dictionary_v0_1",
        label_snapshot="New",
    )

    assert reference.canonical_id == "order_status.new"


def test_local_enum_mapping_requires_canonical_id_when_confirmed() -> None:
    with pytest.raises(ValueError, match="library_canonical_id is required"):
        LocalEnumMapping(
            mapping_id="map_bad",
            local_group="order_status",
            local_value="new",
            library_dictionary_group="order_status",
            mapping_status="confirmed",
        )


def test_local_enum_mapping_supports_manual_review_and_intentionally_local() -> None:
    manual = LocalEnumMapping(
        mapping_id="map_manual",
        local_group="product_service_reference_status",
        local_value="ambiguous_manual_review_required",
        library_dictionary_group="product_service_reference_status",
        mapping_status="manual_review_required",
    )
    local = LocalEnumMapping(
        mapping_id="map_local",
        local_group="source_system",
        local_value="sanitized_demo",
        library_dictionary_group="source_system",
        mapping_status="intentionally_local",
    )

    assert manual.mapping_status == "manual_review_required"
    assert local.mapping_status == "intentionally_local"


def test_dictionary_version_pin_exists() -> None:
    pin = DictionaryVersionPin(
        dictionary_version_pin_id="dict_pin_demo",
        library_dictionary_version="shared_operational_dictionary_v0_1",
    )

    assert pin.status == "active"
