"""Terminal previews for order/workflow/projection foundation."""

from __future__ import annotations

import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from forprint_operational_registry.models.order_workflow import (  # noqa: E402
    AlertEvent,
    AlertRule,
    CalculatorOutputPackageReference,
    MaterialRequirement,
    OperationalOrder,
    OperationalOrderLine,
    PaymentProjection,
    ProductServiceReference,
    WorkflowStage,
)
from forprint_operational_registry.services.order_workflow_demo import (  # noqa: E402
    AlertEvaluationService,
    OperationalReportService,
    demo_workflow_template,
)

from scripts.client_card_preview import key_value_table, render_table  # noqa: E402


def demo_order() -> OperationalOrder:
    """Build demo operational order."""

    return OperationalOrder(
        order_id="order_demo_001",
        client_account_id="acc_demo_org_001",
        client_group_id="grp_demo_001",
        calculator_output_package_id="calc_package_demo_001",
        calculator_calculation_id="calc_demo_001",
        calculator_quote_id="quote_demo_001",
        status="needs_review",
        total_amount_planned=2500.0,
        currency="UAH",
        source_system="sanitized_demo",
        source_ref="demo_request_001",
    )


def demo_order_lines() -> list[OperationalOrderLine]:
    """Build demo order lines."""

    return [
        OperationalOrderLine(
            order_line_id="line_demo_001",
            order_id="order_demo_001",
            line_no=1,
            product_or_service_display_name="Demo product/service line",
            raw_product_or_service_name="Raw demo line name",
            quantity=10,
            unit="pcs",
            line_total_planned=2500.0,
            calculator_line_ref="calc_line_demo_001",
            status="draft",
        )
    ]


def demo_calculator_reference() -> CalculatorOutputPackageReference:
    """Build demo calculator reference."""

    return CalculatorOutputPackageReference(
        calculator_reference_id="calc_ref_demo_001",
        order_id="order_demo_001",
        calculator_output_package_id="calc_package_demo_001",
        calculator_calculation_id="calc_demo_001",
        quote_draft_id="quote_draft_demo_001",
        order_draft_id="order_draft_demo_001",
        schema_version="0.1",
        raw_payload_ref="storage_ref_only",
        validation_status="reference_received",
    )


def demo_product_service_references() -> list[ProductServiceReference]:
    """Build demo product/service references."""

    return [
        ProductServiceReference(
            product_service_reference_id="ps_ref_demo_001",
            order_line_id="line_demo_001",
            display_name="Demo product/service display",
            raw_name="Raw product/service text",
            resolution_status="library_reference_pending",
        )
    ]


def demo_material_requirements() -> list[MaterialRequirement]:
    """Build demo material requirements."""

    return [
        MaterialRequirement(
            material_requirement_id="mat_req_demo_001",
            order_id="order_demo_001",
            order_line_id="line_demo_001",
            material_display_name="Demo material",
            raw_material_name="Raw demo material",
            quantity_planned=12.5,
            unit="m2",
            source_type="calculator_reference",
            source_ref="calc_line_demo_001",
            requirement_status="warehouse_reference_pending",
            required_by=datetime(2026, 6, 10, tzinfo=UTC),
        )
    ]


def demo_payment_projection() -> PaymentProjection:
    """Build demo payment projection."""

    return PaymentProjection(
        payment_projection_id="pay_proj_demo_001",
        order_id="order_demo_001",
        client_account_id="acc_demo_org_001",
        accounting_invoice_ref="invoice_ref_demo_001",
        accounting_payment_ref="payment_ref_demo_001",
        total_amount=2500.0,
        paid_amount=1000.0,
        currency="UAH",
        payment_status="partially_paid",
        due_date=datetime(2026, 6, 9, tzinfo=UTC),
        source_system="sanitized_demo",
    )


def demo_workflow_stages() -> list[WorkflowStage]:
    """Build demo workflow stages."""

    now = datetime(2026, 6, 8, 12, tzinfo=UTC)
    return [
        WorkflowStage(
            workflow_stage_id="wf_stage_demo_prepress",
            order_id="order_demo_001",
            stage_code="prepress",
            stage_name="Prepress",
            stage_order=1,
            status="completed",
            contractor_ref="contractor_ref_demo_001",
            deadline_at=now - timedelta(hours=3),
        ),
        WorkflowStage(
            workflow_stage_id="wf_stage_demo_production",
            order_id="order_demo_001",
            stage_code="production",
            stage_name="Production",
            stage_order=2,
            status="in_progress",
            subcontractor_ref="subcontractor_ref_demo_001",
            deadline_at=now - timedelta(hours=1),
        ),
        WorkflowStage(
            workflow_stage_id="wf_stage_demo_manual",
            order_id="order_demo_001",
            stage_code="manual_review",
            stage_name="Manual Review",
            stage_order=3,
            status="manual_review_required",
            is_manual_stage=True,
            manual_override_reason="Synthetic non-standard requirement.",
        ),
    ]


def demo_alert_rules() -> list[AlertRule]:
    """Build demo alert rules."""

    return [
        AlertRule(
            alert_rule_id="alert_rule_late_stage",
            rule_name="Late workflow stage",
            rule_type="workflow_stage_late",
            target_entity_type="workflow_stage",
            severity="high",
            condition_description="Workflow stage deadline is exceeded.",
            threshold_minutes=0,
        ),
        AlertRule(
            alert_rule_id="alert_rule_payment_overdue",
            rule_name="Payment overdue",
            rule_type="payment_overdue",
            target_entity_type="payment_projection",
            severity="warning",
            condition_description="Payment projection is overdue.",
        ),
        AlertRule(
            alert_rule_id="alert_rule_material_unresolved",
            rule_name="Material unresolved",
            rule_type="material_requirement_unresolved",
            target_entity_type="material_requirement",
            severity="warning",
            condition_description="Material requirement still unresolved.",
        ),
    ]


def demo_alert_events() -> list[AlertEvent]:
    """Build demo alert events."""

    now = datetime(2026, 6, 8, 12, tzinfo=UTC)
    stages = demo_workflow_stages()
    material = demo_material_requirements()[0]
    payment = demo_payment_projection()
    payment.payment_status = "overdue"
    rules = demo_alert_rules()
    evaluator = AlertEvaluationService()

    alerts = [
        evaluator.create_late_stage_alert(stages[1], rules[0], now=now),
        evaluator.create_overdue_payment_alert(payment, rules[1]),
        evaluator.create_unresolved_material_alert(material, rules[2]),
    ]

    return [alert for alert in alerts if alert is not None]


def render_order_preview() -> str:
    """Render order preview."""

    order = demo_order()
    lines = demo_order_lines()
    calculator = demo_calculator_reference()
    product_refs = demo_product_service_references()

    return "\n\n".join(
        [
            "ForPrint Operational Registry — Order Preview",
            key_value_table(
                "OPERATIONAL ORDER",
                {
                    "order_id": order.order_id,
                    "client_account_id": order.client_account_id,
                    "client_group_id": order.client_group_id,
                    "status": order.status,
                    "calculator_output_package_id": order.calculator_output_package_id,
                    "calculator_calculation_id": order.calculator_calculation_id,
                    "calculator_quote_id": order.calculator_quote_id,
                },
                [
                    "order_id",
                    "client_account_id",
                    "client_group_id",
                    "status",
                    "calculator_output_package_id",
                    "calculator_calculation_id",
                    "calculator_quote_id",
                ],
            ),
            render_table(
                "ORDER LINES",
                ["line_id", "line_no", "display", "raw", "qty", "unit", "status"],
                [
                    [
                        line.order_line_id,
                        line.line_no,
                        line.product_or_service_display_name,
                        line.raw_product_or_service_name,
                        line.quantity,
                        line.unit,
                        line.status,
                    ]
                    for line in lines
                ],
            ),
            key_value_table(
                "CALCULATOR REFS",
                {
                    "calculator_reference_id": calculator.calculator_reference_id,
                    "calculator_output_package_id": calculator.calculator_output_package_id,
                    "calculator_calculation_id": calculator.calculator_calculation_id,
                    "raw_payload_ref": calculator.raw_payload_ref,
                    "validation_status": calculator.validation_status,
                },
                [
                    "calculator_reference_id",
                    "calculator_output_package_id",
                    "calculator_calculation_id",
                    "raw_payload_ref",
                    "validation_status",
                ],
            ),
            render_table(
                "PRODUCT/SERVICE REFS",
                ["ref_id", "line_id", "display", "raw", "resolution"],
                [
                    [
                        reference.product_service_reference_id,
                        reference.order_line_id,
                        reference.display_name,
                        reference.raw_name,
                        reference.resolution_status,
                    ]
                    for reference in product_refs
                ],
            ),
        ]
    )


def render_workflow_preview() -> str:
    """Render workflow preview."""

    template = demo_workflow_template()
    stages = demo_workflow_stages()

    return "\n\n".join(
        [
            "ForPrint Operational Registry — Workflow Preview",
            render_table(
                "WORKFLOW TEMPLATE",
                ["code", "name", "order", "duration", "role"],
                [
                    [
                        stage.stage_code,
                        stage.stage_name,
                        stage.default_order,
                        stage.default_duration_minutes,
                        stage.responsible_role,
                    ]
                    for stage in template.stages
                ],
            ),
            render_table(
                "WORKFLOW STAGES",
                [
                    "stage_id",
                    "code",
                    "status",
                    "contractor",
                    "subcontractor",
                    "manual_reason",
                    "late",
                ],
                [
                    [
                        stage.workflow_stage_id,
                        stage.stage_code,
                        stage.status,
                        stage.contractor_ref,
                        stage.subcontractor_ref,
                        stage.manual_override_reason,
                        "yes" if stage.is_late(now=datetime(2026, 6, 8, 12, tzinfo=UTC)) else "no",
                    ]
                    for stage in stages
                ],
            ),
        ]
    )


def render_payment_preview() -> str:
    """Render payment preview."""

    payment = demo_payment_projection()

    return "\n\n".join(
        [
            "ForPrint Operational Registry — Payment Preview",
            key_value_table(
                "PAYMENT PROJECTION",
                {
                    "payment_projection_id": payment.payment_projection_id,
                    "order_id": payment.order_id,
                    "client_account_id": payment.client_account_id,
                    "total_amount": payment.total_amount,
                    "paid_amount": payment.paid_amount,
                    "unpaid_amount": payment.unpaid_amount,
                    "payment_status": payment.payment_status,
                    "accounting_invoice_ref": payment.accounting_invoice_ref,
                    "accounting_payment_ref": payment.accounting_payment_ref,
                },
                [
                    "payment_projection_id",
                    "order_id",
                    "client_account_id",
                    "total_amount",
                    "paid_amount",
                    "unpaid_amount",
                    "payment_status",
                    "accounting_invoice_ref",
                    "accounting_payment_ref",
                ],
            ),
        ]
    )


def render_material_requirement_preview() -> str:
    """Render material requirement preview."""

    requirements = demo_material_requirements()

    return "\n\n".join(
        [
            "ForPrint Operational Registry — Material Requirement Preview",
            render_table(
                "MATERIAL REQUIREMENT",
                [
                    "requirement_id",
                    "order_id",
                    "line_id",
                    "display",
                    "qty",
                    "unit",
                    "status",
                    "warehouse_ref",
                ],
                [
                    [
                        requirement.material_requirement_id,
                        requirement.order_id,
                        requirement.order_line_id,
                        requirement.material_display_name,
                        requirement.quantity_planned,
                        requirement.unit,
                        requirement.requirement_status,
                        requirement.warehouse_reference,
                    ]
                    for requirement in requirements
                ],
            ),
        ]
    )


def render_alert_preview() -> str:
    """Render alert preview."""

    rules = demo_alert_rules()
    alerts = demo_alert_events()

    return "\n\n".join(
        [
            "ForPrint Operational Registry — Alert Preview",
            render_table(
                "ALERT RULES",
                ["rule_id", "name", "type", "severity", "target", "active"],
                [
                    [
                        rule.alert_rule_id,
                        rule.rule_name,
                        rule.rule_type,
                        rule.severity,
                        rule.target_entity_type,
                        "yes" if rule.is_active else "no",
                    ]
                    for rule in rules
                ],
            ),
            render_table(
                "ALERT EVENTS",
                ["event_id", "rule_id", "target", "severity", "status", "notify"],
                [
                    [
                        alert.alert_event_id,
                        alert.alert_rule_id,
                        alert.target_entity_type,
                        alert.severity,
                        alert.status,
                        alert.notification_status,
                    ]
                    for alert in alerts
                ],
            ),
        ]
    )


def render_operational_report_preview() -> str:
    """Render operational report preview."""

    service = OperationalReportService()
    order_projection = service.produce_client_order_history([demo_order()])
    payment_projection = service.produce_payment_debt_summary([demo_payment_projection()])
    workflow_projection = service.produce_workflow_status_summary(demo_workflow_stages())
    alert_projection = service.produce_alert_summary(demo_alert_events())

    projections = [
        order_projection,
        payment_projection,
        workflow_projection,
        alert_projection,
    ]

    rows: list[list[Any]] = []
    for projection in projections:
        rows.append(
            [
                projection.projection_type,
                ", ".join(projection.dimensions),
                ", ".join(projection.metrics),
                len(projection.rows),
            ]
        )

    return "\n\n".join(
        [
            "ForPrint Operational Registry — Operational Report Preview",
            render_table(
                "OPERATIONAL REPORTS",
                ["type", "dimensions", "metrics", "rows"],
                rows,
            ),
        ]
    )


def main() -> int:
    """CLI entrypoint."""

    if len(sys.argv) < 2:
        print(render_order_preview())
        return 0

    command = sys.argv[1]

    renderers = {
        "order": render_order_preview,
        "workflow": render_workflow_preview,
        "payment": render_payment_preview,
        "material": render_material_requirement_preview,
        "alert": render_alert_preview,
        "report": render_operational_report_preview,
    }

    if command not in renderers:
        print(f"Unknown preview command: {command}")
        return 1

    print(renderers[command]())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
