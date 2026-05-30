import pytest
from forprint_operational_registry.models.note import OperationalNote


def test_operational_note_can_be_created() -> None:
    note = OperationalNote(
        note_id="note_001",
        order_id="order_001",
        author_ref="operator_001",
        note_text="Prepare for production.",
    )

    assert note.note_id == "note_001"
    assert note.order_id == "order_001"


def test_operational_note_does_not_become_crm_or_accounting_history() -> None:
    with pytest.raises(ValueError, match="must not become CRM/accounting history"):
        OperationalNote(
            note_id="note_001",
            order_id="order_001",
            author_ref="operator_001",
            note_text="Bad metadata.",
            metadata={"payment_truth": "paid"},
        )


def test_operational_note_metadata_is_immutable() -> None:
    note = OperationalNote(
        note_id="note_001",
        order_id="order_001",
        author_ref="operator_001",
        note_text="Prepare for production.",
        metadata={"kind": "internal"},
    )

    with pytest.raises(TypeError):
        note.metadata["kind"] = "changed"
