"""Internal adapter-facing facade for Operational Registry v0.4.

This facade is not API.
It does not import Gateway/CRM/Telegram/Accounting/Calculator/Prepress code.
It performs no network calls.
"""

from dataclasses import asdict, is_dataclass
from typing import Any
from uuid import uuid4

from forprint_operational_registry.dto.commands import (
    AddOperationalNoteCommand,
    AssignOperationalTaskCommand,
    ChangeTaskStatusCommand,
    CreateOperationalTaskCommand,
)
from forprint_operational_registry.dto.envelope import OperationalCommandEnvelope
from forprint_operational_registry.dto.errors import (
    OperationalError,
    OperationalErrorCode,
    OperationalWarning,
    OperationalWarningCode,
)
from forprint_operational_registry.dto.queries import GetOrderHistoryQuery, GetOrderStateQuery
from forprint_operational_registry.dto.results import (
    OperationalCommandResult,
    OperationalQueryResult,
    OperationalResultStatus,
)
from forprint_operational_registry.repositories.memory import InMemoryRepositoryBundle
from forprint_operational_registry.services.note_registry import OperationalNoteService
from forprint_operational_registry.services.order_lifecycle import InvalidOrderTransition
from forprint_operational_registry.services.order_queries import OrderHistoryQueryService
from forprint_operational_registry.services.order_readiness import OrderReadinessService
from forprint_operational_registry.services.order_registry import OrderRegistryService
from forprint_operational_registry.services.projections import OperationalProjectionService
from forprint_operational_registry.services.task_registry import TaskRegistryService


class OperationalRegistryFacade:
    """Internal surface for future adapters."""

    def __init__(self, repositories: InMemoryRepositoryBundle) -> None:
        self._repositories = repositories
        self._orders = OrderRegistryService(repositories.orders, repositories.events)
        self._tasks = TaskRegistryService(repositories.tasks, repositories.events)
        self._notes = OperationalNoteService(repositories.notes, repositories.events)
        self._history = OrderHistoryQueryService(repositories.events)
        self._readiness = OrderReadinessService(repositories.orders, repositories.blockers)
        self._projections = OperationalProjectionService(
            clients=repositories.clients,
            orders=repositories.orders,
            tasks=repositories.tasks,
            events=repositories.events,
            blockers=repositories.blockers,
        )
        self._processed_command_ids: set[str] = set()

    def handle_create_order(
        self,
        envelope: OperationalCommandEnvelope,
    ) -> OperationalCommandResult:
        """Handle create order envelope."""

        duplicate = self._check_duplicate(envelope)
        if duplicate is not None:
            return duplicate

        try:
            command = envelope.to_create_order_command()
            order = self._orders.create_order(command)
            snapshot = self._order_projection_dict(order.order_id)
            warnings = self._readiness_warnings(order.order_id)

            return self._command_result(
                envelope=envelope,
                status=OperationalResultStatus.APPLIED,
                entity_type="order",
                entity_id=order.order_id,
                state_snapshot=snapshot,
                events_appended=("order_created",),
                warnings=warnings,
            )
        except ValueError as error:
            return self._command_result(
                envelope=envelope,
                status=OperationalResultStatus.VALIDATION_FAILED,
                entity_type=envelope.target_entity_type,
                entity_id=envelope.target_entity_id,
                errors=(
                    OperationalError(
                        code=OperationalErrorCode.VALIDATION_FAILED.value,
                        message=str(error),
                    ),
                ),
            )

    def handle_change_order_status(
        self,
        envelope: OperationalCommandEnvelope,
    ) -> OperationalCommandResult:
        """Handle order status change envelope."""

        duplicate = self._check_duplicate(envelope)
        if duplicate is not None:
            return duplicate

        command = envelope.to_change_order_status_command()

        if self._repositories.orders.get(command.order_id) is None:
            return self._command_result(
                envelope=envelope,
                status=OperationalResultStatus.NOT_FOUND,
                entity_type="order",
                entity_id=command.order_id,
                errors=(
                    OperationalError(
                        code=OperationalErrorCode.ENTITY_NOT_FOUND.value,
                        message=f"Order not found: {command.order_id}",
                    ),
                ),
            )

        if self._repositories.blockers.list_open_by_entity(
            "order", command.order_id
        ) and command.to_status in {"ready_for_production", "in_production"}:
            return self._command_result(
                envelope=envelope,
                status=OperationalResultStatus.BLOCKED,
                entity_type="order",
                entity_id=command.order_id,
                errors=(
                    OperationalError(
                        code=OperationalErrorCode.BLOCKED_BY_ACTIVE_BLOCKER.value,
                        message="Order has active operational blockers.",
                    ),
                ),
            )

        try:
            order = self._orders.change_order_status(command)
            snapshot = self._order_projection_dict(order.order_id)
            warnings = self._readiness_warnings(order.order_id)

            return self._command_result(
                envelope=envelope,
                status=OperationalResultStatus.APPLIED,
                entity_type="order",
                entity_id=order.order_id,
                state_snapshot=snapshot,
                events_appended=("order_status_changed",),
                warnings=warnings,
            )
        except InvalidOrderTransition as error:
            return self._command_result(
                envelope=envelope,
                status=OperationalResultStatus.VALIDATION_FAILED,
                entity_type="order",
                entity_id=command.order_id,
                errors=(
                    OperationalError(
                        code=OperationalErrorCode.INVALID_TRANSITION.value,
                        message=str(error),
                    ),
                ),
            )

    def handle_create_task(
        self,
        command: CreateOperationalTaskCommand,
        command_id: str,
        correlation_id: str,
        idempotency_key: str,
    ) -> OperationalCommandResult:
        """Handle task creation command."""

        task = self._tasks.create_task(command)

        return OperationalCommandResult(
            result_id=f"result_{uuid4().hex}",
            command_id=command_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
            status=OperationalResultStatus.APPLIED.value,
            entity_type="task",
            entity_id=task.task_id,
            events_appended=("task_created",),
        )

    def handle_assign_task(
        self,
        command: AssignOperationalTaskCommand,
        command_id: str,
        correlation_id: str,
        idempotency_key: str,
    ) -> OperationalCommandResult:
        """Handle task assignment command."""

        task = self._tasks.assign_task(command)

        return OperationalCommandResult(
            result_id=f"result_{uuid4().hex}",
            command_id=command_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
            status=OperationalResultStatus.APPLIED.value,
            entity_type="task",
            entity_id=task.task_id,
            events_appended=("task_assigned",),
        )

    def handle_change_task_status(
        self,
        command: ChangeTaskStatusCommand,
        command_id: str,
        correlation_id: str,
        idempotency_key: str,
    ) -> OperationalCommandResult:
        """Handle task status change command."""

        task = self._tasks.change_task_status(command)

        return OperationalCommandResult(
            result_id=f"result_{uuid4().hex}",
            command_id=command_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
            status=OperationalResultStatus.APPLIED.value,
            entity_type="task",
            entity_id=task.task_id,
            events_appended=("task_status_changed",),
        )

    def handle_add_note(
        self,
        command: AddOperationalNoteCommand,
        command_id: str,
        correlation_id: str,
        idempotency_key: str,
    ) -> OperationalCommandResult:
        """Handle add note command."""

        note = self._notes.add_note(command)

        return OperationalCommandResult(
            result_id=f"result_{uuid4().hex}",
            command_id=command_id,
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
            status=OperationalResultStatus.APPLIED.value,
            entity_type="operational_note",
            entity_id=note.note_id,
            events_appended=("operational_note_added",),
        )

    def get_order_state(self, query: GetOrderStateQuery) -> OperationalQueryResult:
        """Return order state projection query result."""

        projection = self._projections.build_order_state_projection(query.order_id)

        return OperationalQueryResult(
            result_id=f"query_{uuid4().hex}",
            correlation_id="local_query",
            status=OperationalResultStatus.APPLIED.value,
            result_type="order_state_projection",
            payload=self._to_plain_dict(projection),
        )

    def get_order_history(self, query: GetOrderHistoryQuery) -> OperationalQueryResult:
        """Return order history query result."""

        history = self._history.get_order_history(query)

        return OperationalQueryResult(
            result_id=f"query_{uuid4().hex}",
            correlation_id="local_query",
            status=OperationalResultStatus.APPLIED.value,
            result_type="order_history",
            payload={
                "order_id": history.order_id,
                "events": [event.event_type for event in history.events],
            },
        )

    def get_order_projection(self, query: GetOrderStateQuery) -> OperationalQueryResult:
        """Return order projection query result."""

        return self.get_order_state(query)

    def get_task_board(self, order_id: str) -> OperationalQueryResult:
        """Return task board query result."""

        projection = self._projections.build_task_board_projection(order_id)

        return OperationalQueryResult(
            result_id=f"query_{uuid4().hex}",
            correlation_id="local_query",
            status=OperationalResultStatus.APPLIED.value,
            result_type="task_board_projection",
            payload={
                "order_id": projection.order_id,
                "tasks": [task.task_id for task in projection.tasks],
                "tasks_by_status": {
                    status: [task.task_id for task in tasks]
                    for status, tasks in projection.tasks_by_status.items()
                },
            },
        )

    def _check_duplicate(
        self,
        envelope: OperationalCommandEnvelope,
    ) -> OperationalCommandResult | None:
        """Detect local duplicate command_id.

        This is not distributed idempotency and not Gateway replacement.
        """

        if envelope.command_id not in self._processed_command_ids:
            self._processed_command_ids.add(envelope.command_id)
            return None

        return self._command_result(
            envelope=envelope,
            status=OperationalResultStatus.NOOP,
            entity_type=envelope.target_entity_type,
            entity_id=envelope.target_entity_id,
            warnings=(
                OperationalWarning(
                    code=OperationalWarningCode.USES_PLACEHOLDER_CONTRACT.value,
                    message="Duplicate command_id detected locally; treated as noop.",
                ),
            ),
            errors=(
                OperationalError(
                    code=OperationalErrorCode.DUPLICATE_COMMAND.value,
                    message=f"Duplicate command_id: {envelope.command_id}",
                ),
            ),
        )

    def _readiness_warnings(self, order_id: str) -> tuple[OperationalWarning, ...]:
        """Return readiness warnings for command result."""

        snapshot = self._readiness.build_readiness_snapshot(order_id)
        warnings: list[OperationalWarning] = []

        if "missing_calculation" in snapshot.missing_references:
            warnings.append(
                OperationalWarning(
                    code=OperationalWarningCode.MISSING_CALCULATION_REFERENCE.value,
                    message="Order has no calculation reference.",
                )
            )

        if "waiting_payment_reference" in snapshot.waiting_reasons:
            warnings.append(
                OperationalWarning(
                    code=OperationalWarningCode.WAITING_PAYMENT_REFERENCE.value,
                    message="Order is waiting for payment reference.",
                )
            )

        return tuple(warnings)

    def _order_projection_dict(self, order_id: str) -> dict[str, Any]:
        """Return order projection as plain dictionary."""

        projection = self._projections.build_order_state_projection(order_id)
        return self._to_plain_dict(projection)

    @staticmethod
    def _to_plain_dict(value: Any) -> dict[str, Any]:
        """Convert dataclass to plain dictionary."""

        if is_dataclass(value):
            return asdict(value)

        if isinstance(value, dict):
            return dict(value)

        raise TypeError(f"Unsupported projection type: {type(value)!r}")

    @staticmethod
    def _command_result(
        envelope: OperationalCommandEnvelope,
        status: OperationalResultStatus,
        entity_type: str,
        entity_id: str,
        state_snapshot: dict[str, Any] | None = None,
        events_appended: tuple[str, ...] = (),
        warnings: tuple[OperationalWarning, ...] = (),
        errors: tuple[OperationalError, ...] = (),
    ) -> OperationalCommandResult:
        """Create command result preserving command boundary metadata."""

        return OperationalCommandResult(
            result_id=f"result_{uuid4().hex}",
            command_id=envelope.command_id,
            correlation_id=envelope.correlation_id,
            idempotency_key=envelope.idempotency_key,
            status=status.value,
            entity_type=entity_type,
            entity_id=entity_id,
            state_snapshot=state_snapshot,
            events_appended=events_appended,
            warnings=warnings,
            errors=errors,
            metadata={
                "source_module": envelope.source_module,
                "source_channel": envelope.source_channel,
                "actor_ref": envelope.actor_ref,
            },
        )
