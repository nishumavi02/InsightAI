"""
Unit tests for Conversation History Persistence Service.
"""

import pytest

from src.database.conversation_service import (
    save_conversation,
    load_conversation_history,
    clear_conversation_history,
)


def test_conversation_persistence(db_connection):
    # Clear prior test entries
    clear_conversation_history(db_connection)

    # Save a turn
    row_id = save_conversation(
        connection=db_connection,
        question="What is total revenue?",
        answer="Total revenue is Rs. 100,000",
        agent_used="SQL",
        confidence=0.95,
    )
    assert row_id > 0

    # Load history
    history = load_conversation_history(db_connection)
    assert len(history) == 1
    assert history[0]["question"] == "What is total revenue?"
    assert history[0]["agent_used"] == "SQL"
    assert history[0]["confidence"] == 0.95

    # Clear history
    clear_conversation_history(db_connection)
    cleared = load_conversation_history(db_connection)
    assert len(cleared) == 0
