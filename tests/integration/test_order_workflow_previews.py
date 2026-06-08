from scripts.order_workflow_preview import (
    render_alert_preview,
    render_material_requirement_preview,
    render_operational_report_preview,
    render_order_preview,
    render_payment_preview,
    render_workflow_preview,
)


def test_order_preview_renders_key_sections() -> None:
    output = render_order_preview()

    assert "ForPrint Operational Registry — Order Preview" in output
    assert "OPERATIONAL ORDER" in output
    assert "ORDER LINES" in output
    assert "CALCULATOR REFS" in output
    assert "PRODUCT/SERVICE REFS" in output


def test_workflow_preview_renders_key_sections() -> None:
    output = render_workflow_preview()

    assert "ForPrint Operational Registry — Workflow Preview" in output
    assert "WORKFLOW TEMPLATE" in output
    assert "WORKFLOW STAGES" in output
    assert "manual_review" in output


def test_payment_preview_renders_key_sections() -> None:
    output = render_payment_preview()

    assert "ForPrint Operational Registry — Payment Preview" in output
    assert "PAYMENT PROJECTION" in output
    assert "unpaid_amount" in output
    assert "accounting_invoice_ref" in output


def test_material_requirement_preview_renders_key_sections() -> None:
    output = render_material_requirement_preview()

    assert "ForPrint Operational Registry — Material Requirement Preview" in output
    assert "MATERIAL REQUIREMENT" in output
    assert "warehouse_reference_pending" in output


def test_alert_preview_renders_key_sections() -> None:
    output = render_alert_preview()

    assert "ForPrint Operational Registry — Alert Preview" in output
    assert "ALERT RULES" in output
    assert "ALERT EVENTS" in output
    assert "not_sent" in output


def test_operational_report_preview_renders_key_sections() -> None:
    output = render_operational_report_preview()

    assert "ForPrint Operational Registry — Operational Report Preview" in output
    assert "OPERATIONAL REPORTS" in output
    assert "client_order_history" in output
    assert "payment_debt_summary" in output
    assert "workflow_stage_status" in output
    assert "alert_summary" in output
