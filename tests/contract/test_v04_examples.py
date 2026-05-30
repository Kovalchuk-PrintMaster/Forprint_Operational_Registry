import json
from pathlib import Path

from forprint_operational_registry.dto.envelope import OperationalCommandEnvelope

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def load_json(relative_path: str) -> dict:
    return json.loads((PROJECT_ROOT / relative_path).read_text(encoding="utf-8"))


def test_all_module_handoff_examples_load() -> None:
    examples = [
        "examples/module_handoffs/telegram_bot/order_intake_draft_to_create_order.json",
        "examples/module_handoffs/crm/manual_order_create_command.json",
        "examples/module_handoffs/gateway/operational_command_envelope_create_order.json",
        "examples/module_handoffs/calculator/attach_quote_result_reference.json",
        "examples/module_handoffs/accounting/payment_reference_confirmed.json",
        "examples/module_handoffs/prepress/prepress_blocker_created.json",
    ]

    for example in examples:
        data = load_json(example)
        assert data["fixture_status"] == "example"
        assert data["real_integration"] is False
        assert data["transport_owner_future"] == "forprint_integration_gateway"
        assert data["canonical_contract_truth_future"] == "forprint_library"


def test_gateway_envelope_example_maps_to_internal_command_shape() -> None:
    data = load_json(
        "examples/module_handoffs/gateway/operational_command_envelope_create_order.json"
    )
    envelope = OperationalCommandEnvelope(**data["envelope"])
    command = envelope.to_create_order_command()

    assert command.order_id == "order_001"
    assert command.client_id == "client_001"


def test_calculator_accounting_and_prepress_examples_use_references_only() -> None:
    calculator = load_json("examples/module_handoffs/calculator/attach_quote_result_reference.json")
    accounting = load_json("examples/module_handoffs/accounting/payment_reference_confirmed.json")
    prepress = load_json("examples/module_handoffs/prepress/prepress_blocker_created.json")

    assert "calculator_result_ref" in calculator["payload"]
    assert "price_calculation" not in calculator["payload"]

    assert "accounting_payment_ref" in accounting["payload"]["metadata"]
    assert "payment_truth" not in accounting["payload"]["metadata"]

    assert "prepress_job_ref" in prepress["payload"]["metadata"]
    assert "prepress_file_lifecycle" not in prepress["payload"]["metadata"]


def test_query_result_examples_load_and_are_boundary_safe() -> None:
    examples = [
        "examples/query_results/order_state_for_crm.json",
        "examples/query_results/order_state_for_telegram.json",
        "examples/query_results/task_board_for_crm.json",
        "examples/query_results/order_timeline_for_operator.json",
        "examples/query_results/order_readiness_snapshot.json",
    ]

    forbidden = {"payment_truth", "invoice_truth", "product_catalog", "material_catalog"}

    for example in examples:
        data = load_json(example)
        assert data["fixture_status"] == "example"
        assert data["schema_version"] == "0.4"
        assert not forbidden.intersection(data["payload"])
