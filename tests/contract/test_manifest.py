from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_manifest_exists() -> None:
    assert (PROJECT_ROOT / "forprint_module_manifest.yaml").exists()


def test_manifest_identity() -> None:
    manifest = yaml.safe_load((PROJECT_ROOT / "forprint_module_manifest.yaml").read_text())

    assert manifest["module_id"] == "forprint_operational_registry"
    assert manifest["role"] == "operational_truth_registry"


def test_manifest_declares_required_boundaries() -> None:
    manifest = yaml.safe_load((PROJECT_ROOT / "forprint_module_manifest.yaml").read_text())
    must_not_own = set(manifest["must_not_own"])

    required = {
        "invoice",
        "payment",
        "accounting_document",
        "material_catalog",
        "product_catalog",
        "price_calculation",
        "prepress_file_lifecycle",
        "uploaded_file_binary_storage",
        "warehouse_stock_balance",
        "integration_routing",
        "library_contract_registry",
        "architecture_governance",
    }

    assert required.issubset(must_not_own)
