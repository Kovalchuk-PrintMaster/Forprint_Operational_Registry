from datetime import UTC, datetime

import pytest
from forprint_operational_registry.models.order_workflow import (
    CalculatorOutputPackageReference,
    OperationalOrder,
    OperationalOrderLine,
    ProductServiceReference,
)


def test_operational_order_can_be_created_with_client_account_ref() -> None:
    order = OperationalOrder(
        order_id="order_demo_001",
        client_account_id="acc_demo_org_001",
        client_group_id="grp_demo_001",
        source_request_id="request_demo_001",
    )

    assert order.order_id == "order_demo_001"
    assert order.client_account_id == "acc_demo_org_001"
    assert order.client_group_id == "grp_demo_001"


def test_operational_order_can_store_calculator_refs_without_dependency() -> None:
    order = OperationalOrder(
        order_id="order_demo_001",
        client_account_id="acc_demo_org_001",
        calculator_output_package_id="calc_package_demo_001",
        calculator_calculation_id="calc_demo_001",
        calculator_quote_id="quote_demo_001",
        calculator_order_draft_id="draft_demo_001",
    )

    assert order.calculator_output_package_id == "calc_package_demo_001"
    assert order.calculator_quote_id == "quote_demo_001"


def test_operational_order_rejects_foreign_truth_payload() -> None:
    with pytest.raises(ValueError, match="must not own foreign-domain truth"):
        OperationalOrder(
            order_id="order_demo_001",
            client_account_id="acc_demo_org_001",
            raw_source_payload={"calculator_formula": "bad"},
        )


def test_operational_order_rejects_invalid_status() -> None:
    with pytest.raises(ValueError, match="Unknown status"):
        OperationalOrder(
            order_id="order_demo_001",
            client_account_id="acc_demo_org_001",
            status="paid",
        )


def test_operational_order_line_supports_display_and_future_library_refs() -> None:
    line = OperationalOrderLine(
        order_line_id="line_demo_001",
        order_id="order_demo_001",
        line_no=1,
        product_or_service_display_name="Demo Display Service",
        raw_product_or_service_name="Raw imported product/service text",
        quantity=10,
        unit="pcs",
        library_product_id="future_library_product_001",
        calculator_line_ref="calc_line_demo_001",
    )

    assert line.product_or_service_display_name == "Demo Display Service"
    assert line.raw_product_or_service_name == "Raw imported product/service text"
    assert line.library_product_id == "future_library_product_001"


def test_operational_order_line_rejects_non_positive_quantity() -> None:
    with pytest.raises(ValueError, match="quantity must be positive"):
        OperationalOrderLine(
            order_line_id="line_demo_001",
            order_id="order_demo_001",
            line_no=1,
            product_or_service_display_name="Demo",
            quantity=0,
            unit="pcs",
        )


def test_calculator_output_package_reference_is_reference_only() -> None:
    received_at = datetime(2026, 6, 8, tzinfo=UTC)

    reference = CalculatorOutputPackageReference(
        calculator_reference_id="calc_ref_demo_001",
        order_id="order_demo_001",
        calculator_output_package_id="calc_package_demo_001",
        calculator_calculation_id="calc_demo_001",
        quote_draft_id="quote_draft_demo_001",
        order_draft_id="order_draft_demo_001",
        schema_version="0.1",
        received_at=received_at,
        raw_payload_ref="storage_ref_only",
        validation_status="reference_received",
    )

    assert reference.source_system == "calculator_engine"
    assert reference.calculator_output_package_id == "calc_package_demo_001"
    assert reference.raw_payload_ref == "storage_ref_only"


def test_calculator_output_package_reference_rejects_non_calculator_source() -> None:
    with pytest.raises(ValueError, match="source_system must be calculator_engine"):
        CalculatorOutputPackageReference(
            calculator_reference_id="calc_ref_demo_001",
            calculator_output_package_id="calc_package_demo_001",
            source_system="manual",
        )


def test_product_service_reference_supports_pending_status() -> None:
    reference = ProductServiceReference(
        product_service_reference_id="ps_ref_demo_001",
        order_line_id="line_demo_001",
        display_name="Demo product/service display",
        raw_name="Raw product/service text",
        resolution_status="library_reference_pending",
    )

    assert reference.display_name == "Demo product/service display"
    assert reference.resolution_status == "library_reference_pending"


def test_product_service_reference_supports_confirmed_library_ref() -> None:
    reference = ProductServiceReference(
        product_service_reference_id="ps_ref_demo_001",
        order_line_id="line_demo_001",
        library_entity_type="product",
        library_entity_id="lib_product_demo_001",
        display_name="Demo product display",
        resolution_status="library_reference_confirmed",
    )

    assert reference.library_entity_id == "lib_product_demo_001"


def test_product_service_reference_requires_library_id_when_confirmed() -> None:
    with pytest.raises(ValueError, match="library_entity_id is required"):
        ProductServiceReference(
            product_service_reference_id="ps_ref_demo_001",
            display_name="Demo product display",
            resolution_status="library_reference_confirmed",
        )


def test_product_service_reference_supports_ambiguous_manual_review() -> None:
    reference = ProductServiceReference(
        product_service_reference_id="ps_ref_demo_ambiguous_001",
        display_name="Ambiguous demo product/service",
        resolution_status="ambiguous_manual_review_required",
        notes="Multiple possible Library entities may match later.",
    )

    assert reference.resolution_status == "ambiguous_manual_review_required"
