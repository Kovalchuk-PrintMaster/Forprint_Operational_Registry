from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_data_foundation_architecture_docs_exist() -> None:
    docs = [
        "docs/architecture/data_foundation_strategy.md",
        "docs/architecture/master_data_policy.md",
        "docs/architecture/operational_fact_policy.md",
        "docs/architecture/event_log_policy.md",
        "docs/architecture/reporting_projection_policy.md",
        "docs/architecture/external_reference_policy.md",
        "docs/architecture/raw_normalized_value_policy.md",
        "docs/architecture/data_history_versioning_policy.md",
        "docs/architecture/one_c_adapter_boundary_policy.md",
        "docs/architecture/entity_card_design_policy.md",
    ]

    for doc in docs:
        assert (PROJECT_ROOT / doc).exists()


def test_data_foundation_examples_load() -> None:
    examples = [
        "master_data_record.example.yaml",
        "operational_fact_record.example.yaml",
        "operational_event_record.example.yaml",
        "external_reference.example.yaml",
        "report_definition.example.yaml",
        "data_projection.example.yaml",
    ]

    for filename in examples:
        path = PROJECT_ROOT / "examples/data_foundation" / filename
        data = yaml.safe_load(path.read_text(encoding="utf-8"))

        assert data["fixture_status"] == "example"
        assert data["contains_real_business_data"] is False


def test_one_c_boundary_doc_prevents_direct_sync_ownership() -> None:
    text = (PROJECT_ROOT / "docs/architecture/one_c_adapter_boundary_policy.md").read_text(
        encoding="utf-8"
    )

    assert "Accounting Registry will later own" in text
    assert "No live 1C write in this step" in text
    assert "No production accounting sync in this step" in text


def test_entity_card_design_policy_mentions_future_cards() -> None:
    text = (PROJECT_ROOT / "docs/architecture/entity_card_design_policy.md").read_text(
        encoding="utf-8"
    )

    assert "stable internal ID" in text
    assert "raw imported fields" in text
    assert "terminal preview behavior" in text
