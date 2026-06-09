from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_dictionary_mapping_architecture_docs_exist() -> None:
    docs = [
        "docs/architecture/library_dictionary_consumption_policy.md",
        "docs/architecture/canonical_status_mapping_policy.md",
        "docs/architecture/local_enum_drift_detection_policy.md",
        "docs/architecture/dictionary_version_pin_policy.md",
        "docs/architecture/operational_registry_dictionary_alignment.md",
    ]

    for doc in docs:
        assert (PROJECT_ROOT / doc).exists()


def test_operational_registry_does_not_claim_library_ownership() -> None:
    text = (
        PROJECT_ROOT / "docs/architecture/operational_registry_dictionary_alignment.md"
    ).read_text(encoding="utf-8")

    assert "ForPrint Library remains the semantic authority" in text
    assert "It does not edit Library" in text
    assert "It does not integrate with Library runtime" in text


def test_mapping_config_preserves_library_boundary() -> None:
    data = yaml.safe_load(
        (
            PROJECT_ROOT / "config/dictionary_mapping/operational_registry_to_library_v0_1.yaml"
        ).read_text(encoding="utf-8")
    )

    assert data["library_authority"] == "forprint_library"
    assert data["runtime_library_dependency"] is False
    assert data["operational_registry_edits_library"] is False
