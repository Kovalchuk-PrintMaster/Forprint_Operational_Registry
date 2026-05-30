from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PLACEHOLDER_DIR = PROJECT_ROOT / "app/forprint_operational_registry/contracts/placeholders"


EXPECTED_PLACEHOLDER_CONTRACTS = {
    "operational.create_order.v1.yaml",
    "operational.change_order_status.v1.yaml",
    "operational.create_task.v1.yaml",
    "operational.assign_task.v1.yaml",
    "operational.add_note.v1.yaml",
    "operational.order_state_snapshot.v1.yaml",
    "operational.order_history_snapshot.v1.yaml",
}


def test_checkpoint_a_placeholder_contracts_exist() -> None:
    existing = {path.name for path in PLACEHOLDER_DIR.glob("*.yaml")}

    assert EXPECTED_PLACEHOLDER_CONTRACTS.issubset(existing)


def test_checkpoint_a_placeholder_contracts_are_non_canonical() -> None:
    for contract_path in PLACEHOLDER_DIR.glob("*.yaml"):
        contract = yaml.safe_load(contract_path.read_text())

        assert contract["fixture_status"] == "placeholder"
        assert contract["canonical_contract_truth"] == "forprint_library_future"
        assert contract["runtime_transport_owner"] == "forprint_integration_gateway_future"
        assert contract["runtime_status"] == "local_offline_fixture_only"
