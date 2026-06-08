from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPORT_ID = (
    "2026-06-05__forprint_operational_registry__report__client-account-card-foundation-v0-1.md"
)
REPORT_PATH = PROJECT_ROOT / "coordination/reports/completion" / REPORT_ID


def test_client_account_checkpoint_c_coordination_files_exist() -> None:
    files = [
        "coordination/status/current_status.yaml",
        "coordination/status/current_status.md",
        "coordination/reports/index.yaml",
        "coordination/reports/completion/2026-06-05__forprint_operational_registry__report__client-account-card-foundation-v0-1.md",
    ]

    for relative_path in files:
        assert (PROJECT_ROOT / relative_path).exists()


def test_current_status_mentions_client_account_phase() -> None:
    data = yaml.safe_load(
        (PROJECT_ROOT / "coordination/status/current_status.yaml").read_text(encoding="utf-8")
    )

    assert data["current_phase"] == "client_account_card_foundation_v0_1"
    assert data["validation"]["make_check"] == "ok"
    assert data["boundaries"]["production_api_added"] is False
    assert data["boundaries"]["real_integrations_added"] is False


def test_makefile_has_required_client_account_targets() -> None:
    text = (PROJECT_ROOT / "Makefile").read_text(encoding="utf-8")

    required_targets = [
        "lint-fix:",
        "status-report:",
        "client-card-preview:",
        "blueprint-pull:",
        "blueprint-check:",
        "blueprint-sync-directives:",
        "coordination-check:",
        "coordination-fix:",
        "module-policy-check:",
    ]

    for target in required_targets:
        assert target in text


def test_completion_report_preserves_boundaries() -> None:
    text = REPORT_PATH.read_text(encoding="utf-8")

    assert "No production API added" in text
    assert "No live 1C write was added" in text
    assert "client_account_id" in text
    assert "Multiple matches do not auto-select an account" in text
