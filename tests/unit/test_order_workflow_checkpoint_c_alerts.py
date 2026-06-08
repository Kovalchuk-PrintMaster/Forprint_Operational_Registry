from datetime import UTC, datetime, timedelta

import pytest
from forprint_operational_registry.models.order_workflow import (
    AlertRule,
    MaterialRequirement,
    PaymentProjection,
    WorkflowStage,
)
from forprint_operational_registry.services.order_workflow_demo import (
    AlertEvaluationService,
)


def test_alert_rule_can_be_created() -> None:
    rule = AlertRule(
        alert_rule_id="alert_rule_demo_001",
        rule_name="Late workflow stage",
        rule_type="workflow_stage_late",
        target_entity_type="workflow_stage",
        severity="high",
        condition_description="Stage deadline exceeded.",
    )

    assert rule.rule_type == "workflow_stage_late"


def test_alert_rule_rejects_negative_threshold() -> None:
    with pytest.raises(ValueError, match="threshold_minutes must not be negative"):
        AlertRule(
            alert_rule_id="alert_rule_demo_001",
            rule_name="Bad threshold",
            rule_type="workflow_stage_late",
            target_entity_type="workflow_stage",
            severity="high",
            condition_description="Bad threshold.",
            threshold_minutes=-1,
        )


def test_alert_evaluation_creates_alert_for_late_stage() -> None:
    now = datetime(2026, 6, 8, 12, tzinfo=UTC)
    stage = WorkflowStage(
        workflow_stage_id="wf_stage_demo_001",
        order_id="order_demo_001",
        stage_code="production",
        stage_name="Production",
        stage_order=1,
        status="in_progress",
        deadline_at=now - timedelta(hours=1),
    )
    rule = AlertRule(
        alert_rule_id="alert_rule_late_stage",
        rule_name="Late workflow stage",
        rule_type="workflow_stage_late",
        target_entity_type="workflow_stage",
        severity="high",
        condition_description="Stage deadline exceeded.",
    )

    alert = AlertEvaluationService().create_late_stage_alert(stage, rule, now=now)

    assert alert is not None
    assert alert.target_entity_type == "workflow_stage"
    assert alert.severity == "high"
    assert alert.notification_status == "not_sent"


def test_alert_evaluation_creates_alert_for_overdue_payment() -> None:
    projection = PaymentProjection(
        payment_projection_id="pay_proj_demo_001",
        order_id="order_demo_001",
        client_account_id="acc_demo_001",
        total_amount=1000.0,
        paid_amount=0.0,
        payment_status="overdue",
    )
    rule = AlertRule(
        alert_rule_id="alert_rule_payment_overdue",
        rule_name="Payment overdue",
        rule_type="payment_overdue",
        target_entity_type="payment_projection",
        severity="warning",
        condition_description="Payment is overdue.",
    )

    alert = AlertEvaluationService().create_overdue_payment_alert(projection, rule)

    assert alert is not None
    assert alert.target_entity_type == "payment_projection"


def test_alert_evaluation_creates_alert_for_unresolved_material_requirement() -> None:
    requirement = MaterialRequirement(
        material_requirement_id="mat_req_demo_001",
        order_id="order_demo_001",
        material_display_name="Demo material",
        quantity_planned=10,
        unit="m2",
        requirement_status="warehouse_reference_pending",
    )
    rule = AlertRule(
        alert_rule_id="alert_rule_material_unresolved",
        rule_name="Material unresolved",
        rule_type="material_requirement_unresolved",
        target_entity_type="material_requirement",
        severity="warning",
        condition_description="Material requirement is unresolved.",
    )

    alert = AlertEvaluationService().create_unresolved_material_alert(requirement, rule)

    assert alert is not None
    assert alert.target_entity_type == "material_requirement"
