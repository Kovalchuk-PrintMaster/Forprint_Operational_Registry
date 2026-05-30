"""Storage model names for Operational Registry v0.5.

The project currently uses lightweight sqlite3 repositories.
These names document persistent entities without introducing ORM lock-in.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StorageEntityName:
    """Storage entity metadata."""

    domain_name: str
    table_name: str


CLIENT_RECORD_STORAGE = StorageEntityName("ClientRecordStorage", "client_records")
ORDER_RECORD_STORAGE = StorageEntityName("OrderRecordStorage", "order_records")
OPERATIONAL_TASK_STORAGE = StorageEntityName("OperationalTaskStorage", "operational_tasks")
OPERATIONAL_EVENT_STORAGE = StorageEntityName("OperationalEventStorage", "operational_events")
OPERATIONAL_NOTE_STORAGE = StorageEntityName("OperationalNoteStorage", "operational_notes")
OPERATIONAL_BLOCKER_STORAGE = StorageEntityName(
    "OperationalBlockerStorage",
    "operational_blockers",
)
