"""SQLite-compatible storage schema for Operational Registry v0.5.

This is a local/test persistence foundation, not production migration system.
"""

STORAGE_STRATEGY_V0 = "repository_boundary_with_memory_and_sqlite"

STORAGE_TABLE_NAMES: tuple[str, ...] = (
    "client_records",
    "order_records",
    "operational_tasks",
    "operational_events",
    "operational_notes",
    "operational_blockers",
)

PLANNED_STORAGE_BACKENDS: tuple[str, ...] = ("postgresql",)

CREATE_TABLE_STATEMENTS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS client_records (
        client_id TEXT PRIMARY KEY,
        display_name TEXT NOT NULL,
        contact_refs_json TEXT NOT NULL,
        source_refs_json TEXT NOT NULL,
        status TEXT NOT NULL,
        metadata_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS order_records (
        order_id TEXT PRIMARY KEY,
        client_id TEXT NOT NULL,
        order_status TEXT NOT NULL,
        workflow_status TEXT NOT NULL,
        source_channel TEXT NOT NULL,
        source_refs_json TEXT NOT NULL,
        quote_ref TEXT,
        accounting_refs_json TEXT NOT NULL,
        production_refs_json TEXT NOT NULL,
        prepress_refs_json TEXT NOT NULL,
        metadata_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS operational_tasks (
        task_id TEXT PRIMARY KEY,
        order_id TEXT NOT NULL,
        task_type TEXT NOT NULL,
        task_status TEXT NOT NULL,
        assigned_to_ref TEXT,
        deadline TEXT,
        blocking_reason TEXT,
        metadata_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS operational_events (
        event_id TEXT PRIMARY KEY,
        entity_type TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        actor_ref TEXT NOT NULL,
        source_module TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS operational_notes (
        note_id TEXT PRIMARY KEY,
        order_id TEXT NOT NULL,
        task_id TEXT,
        author_ref TEXT NOT NULL,
        note_text TEXT NOT NULL,
        visibility TEXT NOT NULL,
        metadata_json TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS operational_blockers (
        blocker_id TEXT PRIMARY KEY,
        entity_type TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        blocker_type TEXT NOT NULL,
        reason TEXT NOT NULL,
        source_module TEXT NOT NULL,
        severity TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        resolved_at TEXT,
        metadata_json TEXT NOT NULL
    )
    """,
)
