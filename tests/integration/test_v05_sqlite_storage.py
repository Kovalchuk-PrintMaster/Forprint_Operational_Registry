from pathlib import Path

from forprint_operational_registry.dto.commands import (
    AddOperationalNoteCommand,
    AssignOperationalTaskCommand,
    ChangeOrderStatusCommand,
    CreateClientCommand,
    CreateOperationalBlockerCommand,
    CreateOperationalTaskCommand,
    CreateOrderCommand,
    ResolveOperationalBlockerCommand,
)
from forprint_operational_registry.repositories.sqlite import SQLiteRepositoryBundle
from forprint_operational_registry.services.blocker_registry import OperationalBlockerService
from forprint_operational_registry.services.client_registry import ClientRegistryService
from forprint_operational_registry.services.note_registry import OperationalNoteService
from forprint_operational_registry.services.order_registry import OrderRegistryService
from forprint_operational_registry.services.task_registry import TaskRegistryService


def sqlite_bundle(tmp_path: Path) -> SQLiteRepositoryBundle:
    return SQLiteRepositoryBundle(tmp_path / "operational_registry_test.sqlite3")


def test_sqlite_storage_initializes_schema(tmp_path: Path) -> None:
    bundle = sqlite_bundle(tmp_path)

    tables = {
        row["name"]
        for row in bundle.connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }

    assert "client_records" in tables
    assert "order_records" in tables
    assert "operational_events" in tables


def test_client_order_task_note_blocker_persist_and_read_back(tmp_path: Path) -> None:
    bundle = sqlite_bundle(tmp_path)

    ClientRegistryService(bundle.clients).create_client(
        CreateClientCommand(client_id="client_001", display_name="Test Client")
    )

    order_service = OrderRegistryService(bundle.orders, bundle.events)
    order_service.create_order(
        CreateOrderCommand(
            order_id="order_001",
            client_id="client_001",
            source_channel="crm_manual",
            quote_ref="quote_001",
        )
    )
    order_service.change_order_status(
        ChangeOrderStatusCommand(
            order_id="order_001",
            to_status="needs_review",
            actor_ref="operator_001",
        )
    )

    task_service = TaskRegistryService(bundle.tasks, bundle.events)
    task_service.create_task(
        CreateOperationalTaskCommand(
            task_id="task_001",
            order_id="order_001",
            task_type="prepress_review",
        )
    )
    task_service.assign_task(
        AssignOperationalTaskCommand(
            task_id="task_001",
            assigned_to_ref="operator_001",
            actor_ref="manager_001",
        )
    )

    OperationalNoteService(bundle.notes, bundle.events).add_note(
        AddOperationalNoteCommand(
            note_id="note_001",
            order_id="order_001",
            author_ref="operator_001",
            note_text="Persistent note.",
        )
    )

    blocker_service = OperationalBlockerService(bundle.blockers, bundle.events)
    blocker_service.create_blocker(
        CreateOperationalBlockerCommand(
            blocker_id="blocker_001",
            entity_type="order",
            entity_id="order_001",
            blocker_type="manual_review_required",
            reason="Persistent blocker.",
        )
    )
    blocker_service.resolve_blocker(
        ResolveOperationalBlockerCommand(
            blocker_id="blocker_001",
            actor_ref="operator_001",
        )
    )

    assert bundle.clients.get("client_001").display_name == "Test Client"
    assert bundle.orders.get("order_001").order_status == "needs_review"
    assert bundle.tasks.get("task_001").assigned_to_ref == "operator_001"
    assert bundle.notes.get("note_001").note_text == "Persistent note."
    assert bundle.blockers.get("blocker_001").status == "resolved"


def test_operational_event_appends_and_reads_back(tmp_path: Path) -> None:
    bundle = sqlite_bundle(tmp_path)

    OrderRegistryService(bundle.orders, bundle.events).create_order(
        CreateOrderCommand(
            order_id="order_001",
            client_id="client_001",
            source_channel="crm_manual",
        )
    )

    events = bundle.events.list_by_entity("order", "order_001")

    assert len(events) == 1
    assert events[0].event_type == "order_created"


def test_order_history_survives_repository_reinstantiation(tmp_path: Path) -> None:
    database_path = tmp_path / "operational_registry_test.sqlite3"
    first_bundle = SQLiteRepositoryBundle(database_path)

    OrderRegistryService(first_bundle.orders, first_bundle.events).create_order(
        CreateOrderCommand(
            order_id="order_001",
            client_id="client_001",
            source_channel="crm_manual",
        )
    )
    first_bundle.close()

    second_bundle = SQLiteRepositoryBundle(database_path)
    events = second_bundle.events.list_by_entity("order", "order_001")

    assert len(events) == 1
    assert events[0].event_type == "order_created"
