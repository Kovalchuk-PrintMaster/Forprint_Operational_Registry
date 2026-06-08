from datetime import UTC, datetime, timedelta

import pytest
from forprint_operational_registry.models.order_workflow import (
    ContractorReference,
    DeadlineControlRecord,
    MaterialRequirement,
    PaymentProjection,
    WorkflowStage,
    WorkflowStageTemplate,
    WorkflowTemplate,
)


def test_material_requirement_supports_planned_quantity_and_unresolved_state() -> None:
    requirement = MaterialRequirement(
        material_requirement_id="mat_req_demo_001",
        order_id="order_demo_001",
        order_line_id="line_demo_001",
        material_display_name="Demo material display",
        raw_material_name="Raw material imported name",
        quantity_planned=12.5,
        unit="m2",
        requirement_status="warehouse_reference_pending",
    )

    assert requirement.quantity_planned == 12.5
    assert requirement.is_unresolved is True
    assert requirement.raw_material_name == "Raw material imported name"


def test_material_requirement_rejects_non_positive_quantity() -> None:
    with pytest.raises(ValueError, match="quantity_planned must be positive"):
        MaterialRequirement(
            material_requirement_id="mat_req_demo_001",
            order_id="order_demo_001",
            material_display_name="Demo",
            quantity_planned=0,
            unit="m2",
        )


def test_payment_projection_calculates_unpaid_amount() -> None:
    projection = PaymentProjection(
        payment_projection_id="pay_proj_demo_001",
        order_id="order_demo_001",
        client_account_id="acc_demo_001",
        total_amount=1000.0,
        paid_amount=250.0,
        payment_status="partially_paid",
        accounting_invoice_ref="invoice_ref_demo_001",
    )

    assert projection.unpaid_amount == 750.0
    assert projection.accounting_invoice_ref == "invoice_ref_demo_001"


def test_payment_projection_rejects_paid_amount_above_total() -> None:
    with pytest.raises(ValueError, match="paid_amount must not exceed total_amount"):
        PaymentProjection(
            payment_projection_id="pay_proj_demo_001",
            order_id="order_demo_001",
            client_account_id="acc_demo_001",
            total_amount=100.0,
            paid_amount=150.0,
        )


def test_workflow_template_creates_ordered_stage_definitions() -> None:
    template = WorkflowTemplate(
        workflow_template_id="wf_template_demo_001",
        template_name="Demo workflow",
        template_type="order",
        version="0.1",
        stages=(
            WorkflowStageTemplate(
                stage_code="production",
                stage_name="Production",
                default_order=2,
            ),
            WorkflowStageTemplate(
                stage_code="prepress",
                stage_name="Prepress",
                default_order=1,
            ),
        ),
    )

    assert template.stages[0].stage_code == "prepress"
    assert template.stages[1].stage_code == "production"


def test_workflow_stage_supports_manual_override() -> None:
    stage = WorkflowStage(
        workflow_stage_id="wf_stage_demo_001",
        order_id="order_demo_001",
        stage_code="manual_check",
        stage_name="Manual Check",
        stage_order=1,
        is_manual_stage=True,
        manual_override_reason="Non-standard customer requirement.",
    )

    assert stage.is_manual_stage is True
    assert stage.manual_override_reason == "Non-standard customer requirement."


def test_workflow_stage_requires_reason_for_manual_stage() -> None:
    with pytest.raises(ValueError, match="manual_override_reason is required"):
        WorkflowStage(
            workflow_stage_id="wf_stage_demo_001",
            order_id="order_demo_001",
            stage_code="manual_check",
            stage_name="Manual Check",
            stage_order=1,
            is_manual_stage=True,
        )


def test_workflow_stage_late_detection_works() -> None:
    now = datetime(2026, 6, 8, 12, 0, tzinfo=UTC)
    stage = WorkflowStage(
        workflow_stage_id="wf_stage_demo_001",
        order_id="order_demo_001",
        stage_code="production",
        stage_name="Production",
        stage_order=1,
        status="in_progress",
        deadline_at=now - timedelta(hours=1),
    )

    assert stage.is_late(now=now) is True


def test_workflow_stage_completed_is_not_late() -> None:
    now = datetime(2026, 6, 8, 12, 0, tzinfo=UTC)
    stage = WorkflowStage(
        workflow_stage_id="wf_stage_demo_001",
        order_id="order_demo_001",
        stage_code="production",
        stage_name="Production",
        stage_order=1,
        status="completed",
        deadline_at=now - timedelta(hours=1),
    )

    assert stage.is_late(now=now) is False


def test_contractor_reference_supports_display_only_and_pending_states() -> None:
    display_only = ContractorReference(
        contractor_reference_id="contractor_ref_demo_001",
        contractor_type="subcontractor",
        display_name="Demo subcontractor display",
        resolution_status="display_only",
    )
    pending = ContractorReference(
        contractor_reference_id="contractor_ref_demo_002",
        contractor_type="subcontractor",
        display_name="Demo subcontractor pending",
        resolution_status="client_account_reference_pending",
    )

    assert display_only.resolution_status == "display_only"
    assert pending.resolution_status == "client_account_reference_pending"


def test_contractor_reference_requires_client_account_when_confirmed() -> None:
    with pytest.raises(ValueError, match="client_account_id is required"):
        ContractorReference(
            contractor_reference_id="contractor_ref_demo_001",
            contractor_type="subcontractor",
            display_name="Demo subcontractor",
            resolution_status="client_account_reference_confirmed",
        )


def test_deadline_control_record_supports_order_stage_payment_material_deadlines() -> None:
    deadline_at = datetime(2026, 6, 8, 18, 0, tzinfo=UTC)

    records = [
        DeadlineControlRecord(
            deadline_control_id="deadline_order_001",
            target_entity_type="order",
            target_entity_id="order_demo_001",
            deadline_type="order_due",
            deadline_at=deadline_at,
        ),
        DeadlineControlRecord(
            deadline_control_id="deadline_stage_001",
            target_entity_type="workflow_stage",
            target_entity_id="wf_stage_demo_001",
            deadline_type="stage_due",
            deadline_at=deadline_at,
        ),
        DeadlineControlRecord(
            deadline_control_id="deadline_payment_001",
            target_entity_type="payment_projection",
            target_entity_id="pay_proj_demo_001",
            deadline_type="payment_due",
            deadline_at=deadline_at,
        ),
        DeadlineControlRecord(
            deadline_control_id="deadline_material_001",
            target_entity_type="material_requirement",
            target_entity_id="mat_req_demo_001",
            deadline_type="material_required_by",
            deadline_at=deadline_at,
        ),
    ]

    assert {record.deadline_type for record in records} == {
        "order_due",
        "stage_due",
        "payment_due",
        "material_required_by",
    }


def test_deadline_control_rejects_negative_warning_window() -> None:
    with pytest.raises(ValueError, match="warning_before_minutes must not be negative"):
        DeadlineControlRecord(
            deadline_control_id="deadline_demo_001",
            target_entity_type="order",
            target_entity_id="order_demo_001",
            deadline_type="order_due",
            deadline_at=datetime(2026, 6, 8, tzinfo=UTC),
            warning_before_minutes=-10,
        )
