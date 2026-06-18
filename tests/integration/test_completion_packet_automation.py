from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import yaml

from scripts.apply_completion_packet import apply_completion_packet, render_completion_report
from scripts.validate_completion_packet import (
    load_completion_packet,
    validate_completion_packet,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_PACKET_PATH = (
    PROJECT_ROOT / "coordination/completion_packets/examples/local_launch_readiness_v0_1.yaml"
)


def _copy_coordination_files(source_root: Path, target_root: Path) -> None:
    for relative_path in (
        "coordination/reports/index.yaml",
        "coordination/status/current_status.yaml",
    ):
        source = source_root / relative_path
        target = target_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def _copy_packet_to_tmp(packet: dict[str, Any], target_root: Path) -> Path:
    packet_path = (
        target_root / "coordination/completion_packets/examples/local_launch_readiness_v0_1.yaml"
    )
    packet_path.parent.mkdir(parents=True, exist_ok=True)
    packet_path.write_text(
        yaml.safe_dump(packet, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return packet_path


def test_completion_packet_example_is_valid() -> None:
    packet = load_completion_packet(EXAMPLE_PACKET_PATH)

    assert validate_completion_packet(packet) == []


def test_completion_report_render_contains_required_sections() -> None:
    packet = load_completion_packet(EXAMPLE_PACKET_PATH)
    report = render_completion_report(packet)

    assert "## Summary" in report
    assert "## Implemented" in report
    assert "## Checks" in report
    assert "## Boundary confirmation" in report
    assert "## Instruction sources reviewed" in report
    assert "## Standards reviewed" in report
    assert "## Standards alignment notes" in report
    assert packet["summary"].strip() in report


def test_apply_completion_packet_is_idempotent(tmp_path: Path) -> None:
    packet = load_completion_packet(EXAMPLE_PACKET_PATH)
    packet = dict(packet)
    packet["report_path"] = (
        "coordination/reports/completion/"
        "test__forprint_operational_registry__report__local-launch-readiness.md"
    )
    packet["report_id"] = "test__forprint_operational_registry__report__local-launch-readiness"

    _copy_coordination_files(PROJECT_ROOT, tmp_path)
    _copy_packet_to_tmp(packet, tmp_path)

    first_changes = apply_completion_packet(packet, tmp_path)
    second_changes = apply_completion_packet(packet, tmp_path)

    assert any(first_changes.values())
    assert not any(second_changes.values())


def test_reports_index_update_does_not_duplicate_report_id(tmp_path: Path) -> None:
    packet = load_completion_packet(EXAMPLE_PACKET_PATH)
    packet = dict(packet)
    packet["report_path"] = (
        "coordination/reports/completion/test__forprint_operational_registry__report__dedupe.md"
    )
    packet["report_id"] = "test__forprint_operational_registry__report__dedupe"

    _copy_coordination_files(PROJECT_ROOT, tmp_path)

    apply_completion_packet(packet, tmp_path)
    apply_completion_packet(packet, tmp_path)

    index = yaml.safe_load(
        (tmp_path / "coordination/reports/index.yaml").read_text(encoding="utf-8")
    )
    matching_reports = [
        report
        for report in index["reports"]
        if isinstance(report, dict) and report.get("report_id") == packet["report_id"]
    ]

    assert len(matching_reports) == 1


def test_current_status_update_contains_new_phase_and_report_id(
    tmp_path: Path,
) -> None:
    packet = load_completion_packet(EXAMPLE_PACKET_PATH)
    packet = dict(packet)
    packet["report_path"] = (
        "coordination/reports/completion/test__forprint_operational_registry__report__status.md"
    )
    packet["report_id"] = "test__forprint_operational_registry__report__status"

    _copy_coordination_files(PROJECT_ROOT, tmp_path)

    apply_completion_packet(packet, tmp_path)

    status = yaml.safe_load(
        (tmp_path / "coordination/status/current_status.yaml").read_text(encoding="utf-8")
    )

    assert status["current_phase"] == packet["phase"]
    assert status["last_report_id"] == packet["report_id"]
    assert status["current_status"] == f"{packet['phase']}_completed"


def test_completion_packet_boundaries_prevent_runtime_scope() -> None:
    packet = load_completion_packet(EXAMPLE_PACKET_PATH)
    boundary = packet["boundary_confirmation"]

    assert boundary["no_production_api"] is True
    assert boundary["no_live_external_integrations"] is True
    assert boundary["no_real_1c_sync"] is True
    assert boundary["no_crm_dashboard"] is True
    assert boundary["no_calculator_final_price_ownership"] is True
    assert boundary["no_library_catalog_ownership"] is True
    assert boundary["no_warehouse_stock_truth"] is True

def test_current_status_md_update_preserves_existing_content(tmp_path: Path) -> None:
    packet = load_completion_packet(EXAMPLE_PACKET_PATH)
    packet = dict(packet)
    packet["report_path"] = (
        "coordination/reports/completion/"
        "test__forprint_operational_registry__report__status-md.md"
    )
    packet["report_id"] = "test__forprint_operational_registry__report__status-md"

    _copy_coordination_files(PROJECT_ROOT, tmp_path)

    status_md = tmp_path / "coordination/status/current_status.md"
    status_md.parent.mkdir(parents=True, exist_ok=True)
    status_md.write_text(
        "# Existing status\n\nKeep this historical content.\n",
        encoding="utf-8",
    )

    first_changes = apply_completion_packet(packet, tmp_path)
    second_changes = apply_completion_packet(packet, tmp_path)

    text = status_md.read_text(encoding="utf-8")

    assert first_changes["current_status_md_changed"] is True
    assert second_changes["current_status_md_changed"] is False
    assert "# Existing status" in text
    assert "Keep this historical content." in text
    assert text.count(f"completion-packet:{packet['report_id']}:status-start") == 1
    assert text.count(f"completion-packet:{packet['report_id']}:status-end") == 1