"""Operational blocker service for Operational Registry v0.3."""

from uuid import uuid4

from forprint_operational_registry.dto.commands import (
    CreateOperationalBlockerCommand,
    ResolveOperationalBlockerCommand,
)
from forprint_operational_registry.models.blockers import OperationalBlocker
from forprint_operational_registry.models.event import OperationalEvent
from forprint_operational_registry.repositories.interfaces import (
    OperationalBlockerRepository,
    OperationalEventRepository,
)


class OperationalBlockerService:
    """Create, resolve and query lightweight operational blockers."""

    def __init__(
        self,
        blockers: OperationalBlockerRepository,
        events: OperationalEventRepository,
    ) -> None:
        self._blockers = blockers
        self._events = events

    def create_blocker(self, command: CreateOperationalBlockerCommand) -> OperationalBlocker:
        """Create operational blocker and append blocker_created event."""

        blocker = OperationalBlocker(
            blocker_id=command.blocker_id,
            entity_type=command.entity_type,
            entity_id=command.entity_id,
            blocker_type=command.blocker_type,
            reason=command.reason,
            source_module=command.source_module,
            severity=command.severity,
            metadata=command.metadata,
        )
        self._blockers.add(blocker)

        self._events.append(
            OperationalEvent(
                event_id=f"evt_{uuid4().hex}",
                entity_type=blocker.entity_type,
                entity_id=blocker.entity_id,
                event_type="operational_blocker_created",
                actor_ref=command.actor_ref,
                source_module=command.source_module,
                payload={
                    "blocker_id": blocker.blocker_id,
                    "blocker_type": blocker.blocker_type,
                    "severity": blocker.severity,
                    "status": blocker.status,
                },
            )
        )

        return blocker

    def resolve_blocker(self, command: ResolveOperationalBlockerCommand) -> OperationalBlocker:
        """Resolve operational blocker and append blocker_resolved event."""

        blocker = self._blockers.get(command.blocker_id)
        if blocker is None:
            raise KeyError(f"Operational blocker not found: {command.blocker_id}")

        previous_status = blocker.status
        blocker.resolve()
        self._blockers.save(blocker)

        self._events.append(
            OperationalEvent(
                event_id=f"evt_{uuid4().hex}",
                entity_type=blocker.entity_type,
                entity_id=blocker.entity_id,
                event_type="operational_blocker_resolved",
                actor_ref=command.actor_ref,
                source_module=command.source_module,
                payload={
                    "blocker_id": blocker.blocker_id,
                    "previous_status": previous_status,
                    "status": blocker.status,
                    "reason": command.reason,
                    "metadata": command.metadata,
                },
            )
        )

        return blocker

    def is_entity_blocked(self, entity_type: str, entity_id: str) -> bool:
        """Return whether entity has open blockers."""

        return bool(self._blockers.list_open_by_entity(entity_type, entity_id))

    def list_open_blockers(
        self,
        entity_type: str,
        entity_id: str,
    ) -> tuple[OperationalBlocker, ...]:
        """List open blockers for entity."""

        return self._blockers.list_open_by_entity(entity_type, entity_id)
