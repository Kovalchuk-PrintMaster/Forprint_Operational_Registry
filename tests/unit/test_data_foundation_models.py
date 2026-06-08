from datetime import UTC, datetime

import pytest
from forprint_operational_registry.models.data_foundation import (
    DataProjection,
    ExternalReference,
    MasterDataRecord,
    OperationalEventRecord,
    OperationalFactRecord,
    RawNormalizedValue,
    ReportDefinition,
)


def test_master_data_record_requires_stable_internal_id() -> None:
    with pytest.raises(ValueError, match="internal_id is required"):
        MasterDataRecord(
            internal_id="",
            entity_type="future_product",
            display_name="Demo Product",
        )


def test_display_name_is_not_canonical_truth() -> None:
    record = MasterDataRecord(
        internal_id="md_demo_001",
        entity_type="future_service",
        display_name="Editable Display Name",
        canonical_name="stable_demo_service",
        raw_source_name="Raw imported service name",
    )

    assert record.internal_id == "md_demo_001"
    assert record.display_name == "Editable Display Name"
    assert record.canonical_name == "stable_demo_service"
    assert record.raw_source_name == "Raw imported service name"


def test_external_reference_supports_1c_bas_without_becoming_primary_id() -> None:
    reference = ExternalReference(
        external_reference_id="ext_demo_001",
        internal_entity_type="client_account",
        internal_entity_id="acc_demo_001",
        external_system="1c_bas",
        external_entity_type="counterparty",
        external_code="000000001",
        external_ref="1c-ref-demo",
        raw_payload={"raw_value": "Raw 1C demo presentation"},
    )

    assert reference.internal_entity_id == "acc_demo_001"
    assert reference.external_code == "000000001"
    assert reference.external_code != reference.internal_entity_id


def test_operational_fact_supports_source_refs_and_business_date() -> None:
    business_date = datetime(2026, 6, 8, tzinfo=UTC)
    fact = OperationalFactRecord(
        fact_id="fact_demo_001",
        fact_type="future_order_line",
        business_date=business_date,
        client_account_id="acc_demo_001",
        source_system="sanitized_demo",
        source_ref="demo_order_ref_001",
    )

    assert fact.business_date == business_date
    assert fact.source_ref == "demo_order_ref_001"


def test_raw_and_normalized_values_can_coexist() -> None:
    value = RawNormalizedValue(
        raw_value="10 шт raw",
        normalized_value="10",
        source_system="sanitized_demo",
        source_ref="demo_ref",
    )

    assert value.raw_value == "10 шт raw"
    assert value.normalized_value == "10"


def test_operational_event_supports_append_only_event_concept() -> None:
    event = OperationalEventRecord(
        event_id="evt_demo_001",
        event_type="order_status_changed",
        target_entity_type="order",
        target_entity_id="order_demo_001",
        payload={"from_status": "new", "to_status": "needs_review"},
    )

    assert event.event_type == "order_status_changed"
    assert event.payload["to_status"] == "needs_review"


def test_data_projection_supports_dimensions_metrics_and_rows() -> None:
    projection = DataProjection(
        projection_id="projection_demo_001",
        projection_type="client_order_history",
        dimensions=("client_account_id", "period"),
        metrics=("order_count",),
        rows=(
            {
                "client_account_id": "acc_demo_001",
                "period": "2026-06",
                "order_count": 3,
            },
        ),
    )

    assert "client_account_id" in projection.dimensions
    assert "order_count" in projection.metrics
    assert projection.rows[0]["order_count"] == 3


def test_report_definition_supports_configurable_fields() -> None:
    definition = ReportDefinition(
        report_definition_id="report_def_demo_001",
        report_name="Demo Report",
        report_type="client_order_history",
        dimensions=("client_account_id", "period"),
        metrics=("order_count",),
        filters={"status": ["completed"]},
        default_period="monthly",
    )

    assert definition.default_period == "monthly"
    assert definition.filters["status"] == ["completed"]
