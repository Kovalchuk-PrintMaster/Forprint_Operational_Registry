"""SQLite session helpers for Operational Registry v0.5."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from forprint_operational_registry.storage.schema import CREATE_TABLE_STATEMENTS


def connect_sqlite(database_path: str | Path) -> sqlite3.Connection:
    """Create SQLite connection with row access enabled."""

    path = str(database_path)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_sqlite_schema(connection: sqlite3.Connection) -> None:
    """Initialize local/test SQLite schema."""

    for statement in CREATE_TABLE_STATEMENTS:
        connection.execute(statement)

    connection.commit()
