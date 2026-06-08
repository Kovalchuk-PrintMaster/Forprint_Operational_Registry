from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_order_workflow_architecture_docs_exist() -> None:
    docs = [
        "docs/architecture/order_workflow_foundation.md",
        "docs/architecture/calculator_output_package_reference_policy.md",
        "docs/architecture/product_service_reference_policy.md",
        "docs/architecture/material_requirement_policy.md",
        "docs/architecture/payment_projection_policy.md",
        "docs/architecture/workflow_stage_policy.md",
        "docs/architecture/contractor_subcontractor_tracking_policy.md",
        "docs/architecture/deadline_alert_policy.md",
        "docs/architecture/operational_report_policy.md",
    ]

    for doc in docs:
        assert (PROJECT_ROOT / doc).exists()


def test_order_workflow_examples_load_and_are_sanitized() -> None:
    examples = [
        "demo_order.yaml",
        "demo_order_lines.yaml",
        "demo_calculator_reference.yaml",
        "demo_product_service_references.yaml",
        "demo_material_requirements.yaml",
        "demo_payment_projection.yaml",
        "demo_workflow_template.yaml",
        "demo_workflow_stages.yaml",
        "demo_contractor_references.yaml",
        "demo_deadlines.yaml",
        "demo_alerts.yaml",
        "demo_report_projections.yaml",
    ]

    for filename in examples:
        path = PROJECT_ROOT / "examples/order_workflow" / filename
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert isinstance(data, dict), f"{filename} must contain YAML mapping"

        assert data["fixture_status"] == "example"
        assert data["contains_real_business_data"] is False


def test_calculator_reference_policy_prevents_formula_ownership() -> None:
    text = (
        PROJECT_ROOT / "docs/architecture/calculator_output_package_reference_policy.md"
    ).read_text(encoding="utf-8")

    assert "Calculator Engine remains owner" in text
    assert "Calculator formulas" in text
    assert "pricing rules" in text


def test_payment_projection_policy_preserves_accounting_boundary() -> None:
    text = (PROJECT_ROOT / "docs/architecture/payment_projection_policy.md").read_text(
        encoding="utf-8"
    )

    assert "Accounting Registry remains owner" in text
    assert "1C posting" in text
    assert "projection/read model only" in text


def test_material_requirement_policy_preserves_warehouse_boundary() -> None:
    text = (PROJECT_ROOT / "docs/architecture/material_requirement_policy.md").read_text(
        encoding="utf-8"
    )

    assert "not warehouse stock truth" in text
    assert "Warehouse module will later own" in text


def test_alert_policy_confirms_no_runtime_notification() -> None:
    text = (PROJECT_ROOT / "docs/architecture/deadline_alert_policy.md").read_text(encoding="utf-8")

    assert "No real Telegram sending" in text
    assert "No CRM popup" in text
