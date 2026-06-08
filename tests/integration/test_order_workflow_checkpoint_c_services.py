from datetime import UTC, datetime

from forprint_operational_registry.models.order_workflow import (
    MaterialRequirement,
    OperationalOrder,
    OperationalOrderLine,
    PaymentProjection,
)
from forprint_operational_registry.services.order_workflow_demo import (
    MaterialRequirementService,
    OperationalReportService,
    OrderWorkflowDemoService,
    PaymentProjectionService,
    WorkflowStageService,
    demo_workflow_template,
)


def test_order_workflow_demo_service_creates_order_and_line() -> None:
    service = OrderWorkflowDemoService()
    order = service.create_order(
        OperationalOrder(
            order_id="order_demo_001",
            client_account_id="acc_demo_001",
        )
    )
    line = service.add_order_line(
        OperationalOrderLine(
            order_line_id="line_demo_001",
            order_id=order.order_id,
            line_no=1,
            product_or_service_display_name="Demo line",
            quantity=1,
            unit="pcs",
        )
    )

    assert line.order_id == order.order_id
    assert service.summarize_order_status()["new"] == 1


def test_workflow_stage_service_creates_stages_from_template() -> None:
    template = demo_workflow_template()
    stages = WorkflowStageService().create_stages_from_template(
        order_id="order_demo_001",
        template=template,
    )

    assert [stage.stage_code for stage in stages] == [
        "prepress",
        "production",
        "quality_check",
    ]


def test_material_requirement_service_lists_unresolved_requirements() -> None:
    service = MaterialRequirementService()
    service.add_material_requirement(
        MaterialRequirement(
            material_requirement_id="mat_req_demo_001",
            order_id="order_demo_001",
            material_display_name="Demo material",
            quantity_planned=10,
            unit="m2",
            requirement_status="warehouse_reference_pending",
            required_by=datetime(2026, 6, 10, tzinfo=UTC),
        )
    )

    assert len(service.list_requirements_by_order("order_demo_001")) == 1
    assert len(service.detect_unresolved_requirements()) == 1


def test_payment_projection_service_summarizes_debt_by_client() -> None:
    service = PaymentProjectionService()
    service.create_payment_projection(
        PaymentProjection(
            payment_projection_id="pay_proj_demo_001",
            order_id="order_demo_001",
            client_account_id="acc_demo_001",
            total_amount=1000.0,
            paid_amount=250.0,
        )
    )

    assert service.summarize_debt_by_client()["acc_demo_001"] == 750.0


def test_operational_report_service_produces_demo_reports() -> None:
    service = OperationalReportService()
    order_projection = service.produce_client_order_history(
        [
            OperationalOrder(
                order_id="order_demo_001",
                client_account_id="acc_demo_001",
                total_amount_planned=1000.0,
            )
        ]
    )
    payment_projection = service.produce_payment_debt_summary(
        [
            PaymentProjection(
                payment_projection_id="pay_proj_demo_001",
                order_id="order_demo_001",
                client_account_id="acc_demo_001",
                total_amount=1000.0,
                paid_amount=250.0,
            )
        ]
    )

    assert order_projection.projection_type == "client_order_history"
    assert payment_projection.projection_type == "payment_debt_summary"
