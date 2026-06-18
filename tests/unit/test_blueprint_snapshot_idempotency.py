from pathlib import Path

import yaml

from scripts.sync_blueprint_instruction_packet import (
    semantic_payload as instruction_semantic_payload,
)
from scripts.sync_blueprint_instruction_packet import (
    write_yaml_if_semantic_changed as write_instruction_snapshot,
)
from scripts.sync_blueprint_standards import (
    semantic_payload as standards_semantic_payload,
)
from scripts.sync_blueprint_standards import (
    write_yaml_if_semantic_changed as write_standards_snapshot,
)


def test_instruction_snapshot_semantic_payload_ignores_timestamps() -> None:
    first = {
        "packet_id": "demo",
        "generated_at": "2026-06-18T01:00:00+00:00",
        "nested": {
            "snapshot_timestamp": "2026-06-18T01:00:00+00:00",
            "value": "same",
        },
    }
    second = {
        "packet_id": "demo",
        "generated_at": "2026-06-18T02:00:00+00:00",
        "nested": {
            "snapshot_timestamp": "2026-06-18T02:00:00+00:00",
            "value": "same",
        },
    }

    assert instruction_semantic_payload(first) == instruction_semantic_payload(second)


def test_standards_snapshot_semantic_payload_ignores_timestamps() -> None:
    first = {
        "snapshot_id": "demo",
        "snapshot_timestamp": "2026-06-18T01:00:00+00:00",
        "reviewed_standards": [{"standard_id": "same"}],
    }
    second = {
        "snapshot_id": "demo",
        "snapshot_timestamp": "2026-06-18T02:00:00+00:00",
        "reviewed_standards": [{"standard_id": "same"}],
    }

    assert standards_semantic_payload(first) == standards_semantic_payload(second)


def test_instruction_snapshot_writer_does_not_rewrite_timestamp_only_change(
    tmp_path: Path,
) -> None:
    path = tmp_path / "blueprint_instruction_packet.yaml"
    original = {
        "packet_id": "demo",
        "generated_at": "old",
        "value": "same",
    }
    updated = {
        "packet_id": "demo",
        "generated_at": "new",
        "value": "same",
    }

    path.write_text(yaml.safe_dump(original, sort_keys=False), encoding="utf-8")

    changed = write_instruction_snapshot(updated, path)

    assert changed is False
    assert yaml.safe_load(path.read_text(encoding="utf-8"))["generated_at"] == "old"


def test_standards_snapshot_writer_does_not_rewrite_timestamp_only_change(
    tmp_path: Path,
) -> None:
    path = tmp_path / "blueprint_standards_snapshot.yaml"
    original = {
        "snapshot_id": "demo",
        "snapshot_timestamp": "old",
        "value": "same",
    }
    updated = {
        "snapshot_id": "demo",
        "snapshot_timestamp": "new",
        "value": "same",
    }

    path.write_text(yaml.safe_dump(original, sort_keys=False), encoding="utf-8")

    changed = write_standards_snapshot(updated, path)

    assert changed is False
    assert yaml.safe_load(path.read_text(encoding="utf-8"))["snapshot_timestamp"] == "old"
