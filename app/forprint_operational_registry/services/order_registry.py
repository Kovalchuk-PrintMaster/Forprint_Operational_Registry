"""Order registry service for Operational Registry v0.2."""

from datetime import UTC, datetime
from uuid import uuid4

from forprint_operational_registry.dto.commands import (
    ChangeOrderStatusCommand,
    CreateOrderCommand,
)
from forprint_operational_registry.models.event import OperationalEvent
from forprint_operational_registry.models.order import OrderRecord
from forprint_operational_registry.repositories.interfaces import (
    OperationalEventRepository,
    OrderRepository,
)
from forprint_operational_registry.services.order_lifecycle import (
    InvalidOrderTransition,
    is_valid_transition,
)


class OrderRegistryService:
    """Create and update canonical operational order state."""

    def __init__(
        self,
        orders: OrderRepository,
        events: OperationalEventRepository,
    ) -> None:
        self._orders = orders
        self._events = events

    def create_order(self, command: CreateOrderCommand) -> OrderRecord:
        """Create operational order and append order_created event."""

        order = OrderRecord(
            order_id=command.order_id,
            client_id=command.client_id,
            source_channel=command.source_channel,
            source_refs=command.source_refs,
            quote_ref=command.quote_ref,
            accounting_refs=command.accounting_refs,
            production_refs=command.production_refs,
            prepress_refs=command.prepress_refs,
            metadata={
                **command.metadata,
                **self._optional_reference_metadata(command),
            },
        )

        self._orders.add(order)

        event = OperationalEvent(
            event_id=f"evt_{uuid4().hex}",
            entity_type="order",
            entity_id=order.order_id,
            event_type="order_created",
            actor_ref=command.actor_ref,
            source_module=command.source_module,
            payload={
                "order_id": order.order_id,
                "client_id": order.client_id,
                "source_channel": order.source_channel,
            },
        )
        self._events.append(event)

        return order

    def change_order_status(self, command: ChangeOrderStatusCommand) -> OrderRecord:
        """Change operational status and append order_status_changed event."""

        order = self._orders.get(command.order_id)
        if order is None:
            raise KeyError(f"Order not found: {command.order_id}")

        from_status = order.order_status

        if not is_valid_transition(from_status, command.to_status):
            raise InvalidOrderTransition(
                f"Invalid order transition: {from_status} -> {command.to_status}"
            )

        order.order_status = command.to_status
        order.workflow_status = command.to_status
        order.updated_at = datetime.now(UTC)
        self._orders.save(order)

        event = OperationalEvent(
            event_id=f"evt_{uuid4().hex}",
            entity_type="order",
            entity_id=order.order_id,
            event_type="order_status_changed",
            actor_ref=command.actor_ref,
            source_module=command.source_module,
            payload={
                "from_status": from_status,
                "to_status": command.to_status,
                "reason": command.reason,
                "metadata": command.metadata,
            },
        )
        self._events.append(event)

        return order

    @staticmethod
    def _optional_reference_metadata(command: CreateOrderCommand) -> dict[str, str]:
        """Store optional foreign references as metadata, not foreign ownership."""

        metadata: dict[str, str] = {}

        if command.calculator_result_ref:
            metadata["calculator_result_ref"] = command.calculator_result_ref

        return metadata
