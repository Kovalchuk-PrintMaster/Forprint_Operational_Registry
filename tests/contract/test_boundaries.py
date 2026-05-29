from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_paid_is_not_used_as_canonical_order_status() -> None:
    config = yaml.safe_load(
        (PROJECT_ROOT / "app/forprint_operational_registry/config/statuses.yaml").read_text()
    )

    assert "paid" not in config["order_statuses"]
    assert "payment_reference_confirmed" in config["order_statuses"]


def test_recommended_source_channels_are_documented() -> None:
    config = yaml.safe_load(
        (PROJECT_ROOT / "app/forprint_operational_registry/config/statuses.yaml").read_text()
    )

    assert {
        "telegram_bot",
        "website",
        "mobile_app",
        "crm_manual",
        "gateway_import",
        "internal_module",
        "legacy_import",
    }.issubset(set(config["recommended_source_channels"]))


def test_required_architecture_docs_exist() -> None:
    required_docs = [
        "docs/architecture/operational_registry_boundaries.md",
        "docs/architecture/operational_vs_accounting_registry.md",
        "docs/architecture/operational_vs_crm.md",
        "docs/architecture/order_lifecycle_v0.md",
    ]

    for relative_path in required_docs:
        assert (PROJECT_ROOT / relative_path).exists()


def test_future_library_driven_lifecycle_is_documented() -> None:
    text = (PROJECT_ROOT / "docs/architecture/order_lifecycle_v0.md").read_text()

    assert "Future order lifecycle may depend" in text
    assert "ForPrint Library" in text
