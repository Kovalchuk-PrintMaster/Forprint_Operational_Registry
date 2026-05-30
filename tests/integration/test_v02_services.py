from forprint_operational_registry.dto.commands import (
    AddOperationalNoteCommand,
    AssignOperationalTaskCommand,
    ChangeOrderStatusCommand,
    CreateClientCommand,
    CreateOperationalTaskCommand,
    CreateOrderCommand,
)
from forprint_operational_registry.dto.queries import GetOrderHistoryQuery, GetOrderStateQuery
from forprint_operational_registry.repositories.memory import InMemoryRepositoryBundle
from forprint_operational_registry.services.client_registry import ClientRegistryService
from forprint_operational_registry.services.note_registry import OperationalNoteService
from forprint_operational_registry.services.order_queries import (
    OrderHistoryQueryService,
    OrderQueryService,
)
from forprint_operational_registry.services.order_registry import OrderRegistryService
from forprint_operational_registry.services.task_registry import TaskRegistryService


def test_create_client_command_creates_client_record_through_service() -> None:
    repositories = InMemoryRepositoryBundle()
    service = ClientRegistryService(repositories.clients)

    client = service.create_client(
        CreateClientCommand(
            client_id="client_001",
            display_name="Test Client",
        )
    )

    assert client.client_id == "client_001"
    assert repositories.clients.get("client_001") == client


def test_create_order_command_creates_order_and_event() -> None:
    repositories = InMemoryRepositoryBundle()
    service = OrderRegistryService(repositories.orders, repositories.events)

    order = service.create_order(
        CreateOrderCommand(
            order_id="order_001",
            client_id="client_001",
            source_channel="telegram_bot",
            quote_ref="quote_001",
        )
    )

    events = repositories.events.list_by_entity("order", "order_001")

    assert order.order_id == "order_001"
    assert order.quote_ref == "quote_001"
    assert events[0].event_type == "order_created"


def test_change_order_status_appends_event_without_mutating_existing_event() -> None:
    repositories = InMemoryRepositoryBundle()
    service = OrderRegistryService(repositories.orders, repositories.events)

    service.create_order(
        CreateOrderCommand(
            order_id="order_001",
            client_id="client_001",
            source_channel="crm_manual",
        )
    )

    first_event = repositories.events.list_by_entity("order", "order_001")[0]
    first_payload_before = dict(first_event.payload)

    order = service.change_order_status(
        ChangeOrderStatusCommand(
            order_id="order_001",
            to_status="needs_review",
            actor_ref="operator_001",
        )
    )

    events = repositories.events.list_by_entity("order", "order_001")

    assert order.order_status == "needs_review"
    assert dict(first_event.payload) == first_payload_before
    assert len(events) == 2
    assert events[1].event_type == "order_status_changed"


def test_create_and_assign_task_through_service() -> None:
    repositories = InMemoryRepositoryBundle()
    service = TaskRegistryService(repositories.tasks, repositories.events)

    task = service.create_task(
        CreateOperationalTaskCommand(
            task_id="task_001",
            order_id="order_001",
            task_type="prepress_review",
        )
    )

    assigned_task = service.assign_task(
        AssignOperationalTaskCommand(
            task_id="task_001",
            assigned_to_ref="operator_001",
            actor_ref="manager_001",
        )
    )

    events = repositories.events.list_by_entity("order", "order_001")

    assert task.task_id == "task_001"
    assert assigned_task.assigned_to_ref == "operator_001"
    assert events[-1].event_type == "task_assigned"


def test_add_operational_note_appends_event() -> None:
    repositories = InMemoryRepositoryBundle()
    service = OperationalNoteService(repositories.notes, repositories.events)

    note = service.add_note(
        AddOperationalNoteCommand(
            note_id="note_001",
            order_id="order_001",
            author_ref="operator_001",
            note_text="Check paper before production.",
        )
    )

    events = repositories.events.list_by_entity("order", "order_001")

    assert note.note_id == "note_001"
    assert events[-1].event_type == "operational_note_added"


def test_order_query_services_return_state_and_history() -> None:
    repositories = InMemoryRepositoryBundle()
    order_service = OrderRegistryService(repositories.orders, repositories.events)
    query_service = OrderQueryService(repositories.orders, repositories.tasks)
    history_service = OrderHistoryQueryService(repositories.events)

    order_service.create_order(
        CreateOrderCommand(
            order_id="order_001",
            client_id="client_001",
            source_channel="website",
        )
    )

    state = query_service.get_order_state(GetOrderStateQuery(order_id="order_001"))
    history = history_service.get_order_history(GetOrderHistoryQuery(order_id="order_001"))

    assert state.order_id == "order_001"
    assert state.source_channel == "website"
    assert len(history.events) == 1
