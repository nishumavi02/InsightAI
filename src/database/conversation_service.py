"""
Conversation History Service for InsightAI

Manages persistent chat conversations stored in the SQLite database.
"""

import sqlite3
from typing import List, Dict, Any, Optional


def init_conversation_table(connection: sqlite3.Connection):
    """Ensure the conversation_history table and all required columns exist."""
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    # Check for schema migration columns
    cursor.execute("PRAGMA table_info(conversation_history)")
    existing_cols = {col[1] for col in cursor.fetchall()}

    if "agent_used" not in existing_cols:
        cursor.execute("ALTER TABLE conversation_history ADD COLUMN agent_used TEXT DEFAULT 'ORCHESTRATOR'")
    if "confidence" not in existing_cols:
        cursor.execute("ALTER TABLE conversation_history ADD COLUMN confidence REAL DEFAULT 1.0")

    connection.commit()


def save_conversation(
    connection: sqlite3.Connection,
    question: str,
    answer: str,
    agent_used: str = "ORCHESTRATOR",
    confidence: float = 1.0,
) -> int:
    """
    Save a conversation turn into SQLite and commit immediately.
    """
    init_conversation_table(connection)
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO conversation_history (
            question,
            answer,
            agent_used,
            confidence
        )
        VALUES (?, ?, ?, ?)
        """,
        (question.strip(), answer.strip(), agent_used, confidence),
    )
    connection.commit()
    return cursor.lastrowid


def load_conversation_history(
    connection: sqlite3.Connection,
    limit: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Load stored conversation history ordered chronologically.
    """
    init_conversation_table(connection)
    cursor = connection.cursor()
    query = """
        SELECT
            id,
            question,
            answer,
            agent_used,
            confidence,
            created_at
        FROM conversation_history
        ORDER BY id ASC
    """
    if limit:
        query += f" LIMIT {int(limit)}"

    cursor.execute(query)
    rows = cursor.fetchall()

    history = []
    for row in rows:
        history.append(
            {
                "id": row[0],
                "question": row[1],
                "answer": row[2],
                "agent_used": row[3] or "ORCHESTRATOR",
                "confidence": row[4] if row[4] is not None else 1.0,
                "created_at": str(row[5]),
            }
        )

    return history


def clear_conversation_history(connection: sqlite3.Connection) -> int:
    """Clear all records from conversation_history table."""
    init_conversation_table(connection)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM conversation_history")
    count = cursor.rowcount
    connection.commit()
    return count
