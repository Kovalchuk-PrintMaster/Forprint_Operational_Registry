"""SQLite-backed repositories for Operational Registry v0.5.

SQLite is local/test persistent storage only.
Production PostgreSQL deployment and migrations are not approved in v0.5.
"""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from forprint_operational_registry.models.blockers import OperationalBlocker
from forprint_operational_registry.models.client import ClientRecord
from forprint_operational_registry.models.event import OperationalEvent
from forprint_operational_registry.models.note import OperationalNote
from forprint_operational_registry.models.order import OrderRecord
from forprint_operational_registry.models.task import OperationalTask
from forprint_operational_registry.storage.session import connect_sqlite, initialize_sqlite_schema


def to_jsonable(value: Any) -> Any:
    """Convert value to JSON-compatible structure."""

    if isinstance(value, Mapping):
        return {key: to_jsonable(item) for key, item in value.items()}

    if isinstance(value, list | tuple):
        return [to_jsonable(item) for item in value]

    if isinstance(value, datetime):
        return value.isoformat()

    return value


def json_dump(value: Any) -> str:
    """Dump JSON value."""

    return json.dumps(to_jsonable(value), ensure_ascii=False, sort_keys=True)


def json_load(value: str | None, default: Any) -> Any:
    """Load JSON value."""

    if not value:
        return default

    return json.loads(value)


def dt_to_text(value: datetime | None) -> str | None:
    """Serialize datetime."""

    if value is None:
        return None

    return value.isoformat()


def dt_from_text(value: str | None) -> datetime | None:
    """Deserialize datetime."""

    if not value:
        return None

    return datetime.fromisoformat(value)


class SQLiteClientRepository:
    """SQLite client repository."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add(self, client: ClientRecord) -> None:
        self._connection.execute(
            """
            INSERT OR REPLACE INTO client_records (
                client_id,
                display_name,
                contact_refs_json,
                source_refs_json,
                status,
                metadata_json,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                client.client_id,
                client.display_name,
                json_dump(client.contact_refs),
                json_dump(client.source_refs),
                client.status,
                json_dump(client.metadata),
                client.created_at.isoformat(),
                client.updated_at.isoformat(),
            ),
        )
        self._connection.commit()

    def get(self, client_id: str) -> ClientRecord | None:
        row = self._connection.execute(
            "SELECT * FROM client_records WHERE client_id = ?",
            (client_id,),
        ).fetchone()

        if row is None:
            return None

        return ClientRecord(
            client_id=row["client_id"],
            display_name=row["display_name"],
            contact_refs=json_load(row["contact_refs_json"], []),
            source_refs=json_load(row["source_refs_json"], {}),
            status=row["status"],
            metadata=json_load(row["metadata_json"], {}),
            created_at=dt_from_text(row["created_at"]),
            updated_at=dt_from_text(row["updated_at"]),
        )


class SQLiteOrderRepository:
    """SQLite order repository."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add(self, order: OrderRecord) -> None:
        self.save(order)

    def save(self, order: OrderRecord) -> None:
        self._connection.execute(
            """
            INSERT OR REPLACE INTO order_records (
                order_id,
                client_id,
                order_status,
                workflow_status,
                source_channel,
                source_refs_json,
                quote_ref,
                accounting_refs_json,
                production_refs_json,
                prepress_refs_json,
                metadata_json,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                order.order_id,
                order.client_id,
                order.order_status,
                order.workflow_status,
                order.source_channel,
                json_dump(order.source_refs),
                order.quote_ref,
                json_dump(order.accounting_refs),
                json_dump(order.production_refs),
                json_dump(order.prepress_refs),
                json_dump(order.metadata),
                order.created_at.isoformat(),
                order.updated_at.isoformat(),
            ),
        )
        self._connection.commit()

    def get(self, order_id: str) -> OrderRecord | None:
        row = self._connection.execute(
            "SELECT * FROM order_records WHERE order_id = ?",
            (order_id,),
        ).fetchone()

        if row is None:
            return None

        return self._row_to_order(row)

    def list_by_client(self, client_id: str) -> tuple[OrderRecord, ...]:
        rows = self._connection.execute(
            "SELECT * FROM order_records WHERE client_id = ? ORDER BY created_at",
            (client_id,),
        ).fetchall()

        return tuple(self._row_to_order(row) for row in rows)

    def list_by_status(self, order_status: str) -> tuple[OrderRecord, ...]:
        rows = self._connection.execute(
            "SELECT * FROM order_records WHERE order_status = ? ORDER BY created_at",
            (order_status,),
        ).fetchall()

        return tuple(self._row_to_order(row) for row in rows)

    @staticmethod
    def _row_to_order(row: sqlite3.Row) -> OrderRecord:
        return OrderRecord(
            order_id=row["order_id"],
            client_id=row["client_id"],
            order_status=row["order_status"],
            workflow_status=row["workflow_status"],
            source_channel=row["source_channel"],
            source_refs=json_load(row["source_refs_json"], {}),
            quote_ref=row["quote_ref"],
            accounting_refs=json_load(row["accounting_refs_json"], {}),
            production_refs=json_load(row["production_refs_json"], {}),
            prepress_refs=json_load(row["prepress_refs_json"], {}),
            metadata=json_load(row["metadata_json"], {}),
            created_at=dt_from_text(row["created_at"]),
            updated_at=dt_from_text(row["updated_at"]),
        )


class SQLiteTaskRepository:
    """SQLite task repository."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add(self, task: OperationalTask) -> None:
        self.save(task)

    def save(self, task: OperationalTask) -> None:
        self._connection.execute(
            """
            INSERT OR REPLACE INTO operational_tasks (
                task_id,
                order_id,
                task_type,
                task_status,
                assigned_to_ref,
                deadline,
                blocking_reason,
                metadata_json,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task.task_id,
                task.order_id,
                task.task_type,
                task.task_status,
                task.assigned_to_ref,
                dt_to_text(task.deadline),
                task.blocking_reason,
                json_dump(task.metadata),
                task.created_at.isoformat(),
                task.updated_at.isoformat(),
            ),
        )
        self._connection.commit()

    def get(self, task_id: str) -> OperationalTask | None:
        row = self._connection.execute(
            "SELECT * FROM operational_tasks WHERE task_id = ?",
            (task_id,),
        ).fetchone()

        if row is None:
            return None

        return self._row_to_task(row)

    def list_by_order(self, order_id: str) -> tuple[OperationalTask, ...]:
        rows = self._connection.execute(
            "SELECT * FROM operational_tasks WHERE order_id = ? ORDER BY created_at",
            (order_id,),
        ).fetchall()

        return tuple(self._row_to_task(row) for row in rows)

    @staticmethod
    def _row_to_task(row: sqlite3.Row) -> OperationalTask:
        return OperationalTask(
            task_id=row["task_id"],
            order_id=row["order_id"],
            task_type=row["task_type"],
            task_status=row["task_status"],
            assigned_to_ref=row["assigned_to_ref"],
            deadline=dt_from_text(row["deadline"]),
            blocking_reason=row["blocking_reason"],
            metadata=json_load(row["metadata_json"], {}),
            created_at=dt_from_text(row["created_at"]),
            updated_at=dt_from_text(row["updated_at"]),
        )


class SQLiteOperationalEventRepository:
    """Append-only SQLite operational event repository."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def append(self, event: OperationalEvent) -> None:
        self._connection.execute(
            """
            INSERT INTO operational_events (
                event_id,
                entity_type,
                entity_id,
                event_type,
                actor_ref,
                source_module,
                payload_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.event_id,
                event.entity_type,
                event.entity_id,
                event.event_type,
                event.actor_ref,
                event.source_module,
                json_dump(event.payload),
                event.created_at.isoformat(),
            ),
        )
        self._connection.commit()

    def list_by_entity(self, entity_type: str, entity_id: str) -> tuple[OperationalEvent, ...]:
        rows = self._connection.execute(
            """
            SELECT * FROM operational_events
            WHERE entity_type = ? AND entity_id = ?
            ORDER BY created_at, event_id
            """,
            (entity_type, entity_id),
        ).fetchall()

        return tuple(
            OperationalEvent(
                event_id=row["event_id"],
                entity_type=row["entity_type"],
                entity_id=row["entity_id"],
                event_type=row["event_type"],
                actor_ref=row["actor_ref"],
                source_module=row["source_module"],
                payload=json_load(row["payload_json"], {}),
                created_at=dt_from_text(row["created_at"]),
            )
            for row in rows
        )


class SQLiteOperationalNoteRepository:
    """SQLite operational note repository."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add(self, note: OperationalNote) -> None:
        self._connection.execute(
            """
            INSERT OR REPLACE INTO operational_notes (
                note_id,
                order_id,
                task_id,
                author_ref,
                note_text,
                visibility,
                metadata_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                note.note_id,
                note.order_id,
                note.task_id,
                note.author_ref,
                note.note_text,
                note.visibility,
                json_dump(note.metadata),
                note.created_at.isoformat(),
            ),
        )
        self._connection.commit()

    def get(self, note_id: str) -> OperationalNote | None:
        row = self._connection.execute(
            "SELECT * FROM operational_notes WHERE note_id = ?",
            (note_id,),
        ).fetchone()

        if row is None:
            return None

        return OperationalNote(
            note_id=row["note_id"],
            order_id=row["order_id"],
            task_id=row["task_id"],
            author_ref=row["author_ref"],
            note_text=row["note_text"],
            visibility=row["visibility"],
            metadata=json_load(row["metadata_json"], {}),
            created_at=dt_from_text(row["created_at"]),
        )

    def list_by_order(self, order_id: str) -> tuple[OperationalNote, ...]:
        rows = self._connection.execute(
            "SELECT * FROM operational_notes WHERE order_id = ? ORDER BY created_at",
            (order_id,),
        ).fetchall()

        return tuple(
            OperationalNote(
                note_id=row["note_id"],
                order_id=row["order_id"],
                task_id=row["task_id"],
                author_ref=row["author_ref"],
                note_text=row["note_text"],
                visibility=row["visibility"],
                metadata=json_load(row["metadata_json"], {}),
                created_at=dt_from_text(row["created_at"]),
            )
            for row in rows
        )


class SQLiteOperationalBlockerRepository:
    """SQLite operational blocker repository."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add(self, blocker: OperationalBlocker) -> None:
        self.save(blocker)

    def save(self, blocker: OperationalBlocker) -> None:
        self._connection.execute(
            """
            INSERT OR REPLACE INTO operational_blockers (
                blocker_id,
                entity_type,
                entity_id,
                blocker_type,
                reason,
                source_module,
                severity,
                status,
                created_at,
                resolved_at,
                metadata_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                blocker.blocker_id,
                blocker.entity_type,
                blocker.entity_id,
                blocker.blocker_type,
                blocker.reason,
                blocker.source_module,
                blocker.severity,
                blocker.status,
                blocker.created_at.isoformat(),
                dt_to_text(blocker.resolved_at),
                json_dump(blocker.metadata),
            ),
        )
        self._connection.commit()

    def get(self, blocker_id: str) -> OperationalBlocker | None:
        row = self._connection.execute(
            "SELECT * FROM operational_blockers WHERE blocker_id = ?",
            (blocker_id,),
        ).fetchone()

        if row is None:
            return None

        return self._row_to_blocker(row)

    def list_by_entity(self, entity_type: str, entity_id: str) -> tuple[OperationalBlocker, ...]:
        rows = self._connection.execute(
            """
            SELECT * FROM operational_blockers
            WHERE entity_type = ? AND entity_id = ?
            ORDER BY created_at
            """,
            (entity_type, entity_id),
        ).fetchall()

        return tuple(self._row_to_blocker(row) for row in rows)

    def list_open_by_entity(
        self,
        entity_type: str,
        entity_id: str,
    ) -> tuple[OperationalBlocker, ...]:
        rows = self._connection.execute(
            """
            SELECT * FROM operational_blockers
            WHERE entity_type = ? AND entity_id = ? AND status = 'open'
            ORDER BY created_at
            """,
            (entity_type, entity_id),
        ).fetchall()

        return tuple(self._row_to_blocker(row) for row in rows)

    @staticmethod
    def _row_to_blocker(row: sqlite3.Row) -> OperationalBlocker:
        return OperationalBlocker(
            blocker_id=row["blocker_id"],
            entity_type=row["entity_type"],
            entity_id=row["entity_id"],
            blocker_type=row["blocker_type"],
            reason=row["reason"],
            source_module=row["source_module"],
            severity=row["severity"],
            status=row["status"],
            created_at=dt_from_text(row["created_at"]),
            resolved_at=dt_from_text(row["resolved_at"]),
            metadata=json_load(row["metadata_json"], {}),
        )


@dataclass
class SQLiteRepositoryBundle:
    """SQLite repository bundle for local/test persistence."""

    database_path: str | Path

    def __post_init__(self) -> None:
        self.connection = connect_sqlite(self.database_path)
        initialize_sqlite_schema(self.connection)
        self.clients = SQLiteClientRepository(self.connection)
        self.orders = SQLiteOrderRepository(self.connection)
        self.tasks = SQLiteTaskRepository(self.connection)
        self.events = SQLiteOperationalEventRepository(self.connection)
        self.notes = SQLiteOperationalNoteRepository(self.connection)
        self.blockers = SQLiteOperationalBlockerRepository(self.connection)

    def close(self) -> None:
        """Close SQLite connection."""

        self.connection.close()
