from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXAMPLES_DIR = PROJECT_ROOT / "examples/client_cards"


def load_example(filename: str) -> dict:
    data = yaml.safe_load((EXAMPLES_DIR / filename).read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_client_card_examples_load() -> None:
    examples = [
        "demo_organization_client.yaml",
        "demo_person_client.yaml",
        "demo_ambiguous_phone_lookup.yaml",
    ]

    for example in examples:
        data = load_example(example)
        assert data["fixture_status"] == "example"
        assert data["contains_real_customer_data"] is False


def test_organization_example_preserves_raw_imported_values() -> None:
    data = load_example("demo_organization_client.yaml")

    assert data["client_account"]["client_account_id"] == "acc_demo_org_001"
    assert data["client_account"]["legacy_raw_name"]
    assert data["external_accounting_references"][0]["raw_payload"]["raw_1c_code"]


def test_ambiguous_phone_example_demonstrates_phone_not_canonical_truth() -> None:
    data = load_example("demo_ambiguous_phone_lookup.yaml")

    assert data["lookup_key"]["lookup_type"] == "normalized_phone"
    assert len(data["client_accounts"]) == 2
    assert len(data["account_contact_links"]) == 2
