import sqlite3
from typing import List, Optional

DB_FILE = "addresses.db"


def get_connection():
    """Creates and returns a connection to the SQLite database."""
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Creates the table only if it does not already exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            description TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def insert_address(name: str, latitude: float, longitude: float, description: Optional[str]) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO addresses (name, latitude, longitude, description) VALUES (?, ?, ?, ?)",
        (name, latitude, longitude, description),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def fetch_address(address_id: int) -> Optional[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM addresses WHERE id = ?", (address_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def fetch_all_addresses() -> List[sqlite3.Row]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM addresses")
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_address(address_id: int, name: str, latitude: float, longitude: float, description: Optional[str]) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE addresses
        SET name = ?, latitude = ?, longitude = ?, description = ?
        WHERE id = ?
        """,
        (name, latitude, longitude, description, address_id),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def delete_address(address_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM addresses WHERE id = ?", (address_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted
