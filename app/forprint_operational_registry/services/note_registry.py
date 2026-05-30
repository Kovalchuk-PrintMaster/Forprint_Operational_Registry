"""Operational note service for Operational Registry v0.2."""

from uuid import uuid4

from forprint_operational_registry.dto.commands import AddOperationalNoteCommand
from forprint_operational_registry.models.event import OperationalEvent
from forprint_operational_registry.models.note import OperationalNote
from forprint_operational_registry.repositories.interfaces import (
    OperationalEventRepository,
    OperationalNoteRepository,
)


class OperationalNoteService:
    """Add lightweight operational notes."""

    def __init__(
        self,
        notes: OperationalNoteRepository,
        events: OperationalEventRepository,
    ) -> None:
        self._notes = notes
        self._events = events

    def add_note(self, command: AddOperationalNoteCommand) -> OperationalNote:
        """Add note and append operational_note_added event."""

        note = OperationalNote(
            note_id=command.note_id,
            order_id=command.order_id,
            task_id=command.task_id,
            author_ref=command.author_ref,
            note_text=command.note_text,
            visibility=command.visibility,
            metadata=command.metadata,
        )

        self._notes.add(note)

        self._events.append(
            OperationalEvent(
                event_id=f"evt_{uuid4().hex}",
                entity_type="order",
                entity_id=note.order_id,
                event_type="operational_note_added",
                actor_ref=note.author_ref,
                source_module=command.source_module,
                payload={
                    "note_id": note.note_id,
                    "task_id": note.task_id,
                    "visibility": note.visibility,
                },
            )
        )

        return note
