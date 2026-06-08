from pathlib import Path

import yaml

from scripts.client_card_preview import render_client_card_preview

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_terminal_preview_renders_key_sections() -> None:
    example_path = PROJECT_ROOT / "examples/client_cards/demo_organization_client.yaml"
    data = yaml.safe_load(example_path.read_text(encoding="utf-8"))

    output = render_client_card_preview(data)

    assert "ForPrint Operational Registry — Client Card Preview" in output
    assert "CLIENT ACCOUNT" in output
    assert "CONTACT METHODS" in output
    assert "CONTACT PERSONS" in output
    assert "ACCOUNT-CONTACT LINKS" in output
    assert "ADDRESSES" in output
    assert "LEGAL PROFILE" in output
    assert "EXTERNAL ACCOUNTING REFERENCES" in output
    assert "CONTRACTS" in output
    assert "NOTES / PREFERENCES" in output
    assert "acc_demo_org_001" in output
    assert "+380XXXXXXXXX" in output
