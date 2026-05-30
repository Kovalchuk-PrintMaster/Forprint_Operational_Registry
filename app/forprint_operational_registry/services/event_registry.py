"""Operational event service for append-only event recording."""

from forprint_operational_registry.dto.commands import AppendOperationalEventCommand
from forprint_operational_registry.models.event import OperationalEvent
from forprint_operational_registry.repositories.interfaces import OperationalEventRepository


class OperationalEventService:
    """Append operational events without mutating existing history."""

    def __init__(self, events: OperationalEventRepository) -> None:
        self._events = events

    def append_event(self, command: AppendOperationalEventCommand) -> OperationalEvent:
        """Append operational event."""

        event = OperationalEvent(
            event_id=command.event_id,
            entity_type=command.entity_type,
            entity_id=command.entity_id,
            event_type=command.event_type,
            actor_ref=command.actor_ref,
            source_module=command.source_module,
            payload=command.payload,
        )
        self._events.append(event)
        return event
