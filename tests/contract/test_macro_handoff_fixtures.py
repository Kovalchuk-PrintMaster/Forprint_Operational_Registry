import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
HANDOFF_DIR = PROJECT_ROOT / "examples/handoffs"


def load_fixture(filename: str) -> dict:
    return json.loads((HANDOFF_DIR / filename).read_text(encoding="utf-8"))


def test_handoff_fixtures_load() -> None:
    expected = [
        "telegram_order_intake_to_create_order.json",
        "crm_manual_order_to_create_order.json",
        "calculator_quote_ref_attached_to_order.json",
        "accounting_payment_reference_update.json",
        "prepress_blocker_attached_to_order.json",
    ]

    for filename in expected:
        fixture = load_fixture(filename)
        assert fixture["fixture_status"] == "example"
        assert fixture["runtime_transport_owner"] == "forprint_integration_gateway_future"
        assert fixture["canonical_contract_truth"] == "forprint_library_future"


def test_telegram_order_intake_fixture_maps_to_create_order_shape() -> None:
    fixture = load_fixture("telegram_order_intake_to_create_order.json")

    assert fixture["command_type"] == "operational.create_order.v1"
    assert fixture["payload"]["source_channel"] == "telegram_bot"
    assert "client_id" in fixture["payload"]


def test_calculator_quote_reference_fixture_uses_reference_only() -> None:
    fixture = load_fixture("calculator_quote_ref_attached_to_order.json")
    payload = fixture["payload"]

    assert "quote_ref" in payload
    assert "calculator_result_ref" in payload
    assert "price_calculation" not in payload
    assert "quote_formula" not in payload


def test_accounting_payment_reference_fixture_uses_reference_only() -> None:
    fixture = load_fixture("accounting_payment_reference_update.json")
    metadata = fixture["payload"]["metadata"]

    assert "accounting_invoice_ref" in metadata
    assert "accounting_payment_ref" in metadata
    assert "payment_balance" not in metadata
    assert "invoice_truth" not in metadata


def test_prepress_blocker_fixture_uses_reference_and_blocker_only() -> None:
    fixture = load_fixture("prepress_blocker_attached_to_order.json")
    payload = fixture["payload"]

    assert payload["blocker_type"] == "waiting_prepress_check"
    assert "prepress_job_ref" in payload["metadata"]
    assert "prepress_file_lifecycle" not in payload["metadata"]
