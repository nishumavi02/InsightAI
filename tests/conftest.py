"""
Pytest configuration and shared fixtures for InsightAI test suite.
"""

import sqlite3
import pytest
from pathlib import Path

from src.config import DATABASE_FILE, DOCUMENTS_DIR
from src.database.load_data import init_db


@pytest.fixture(scope="session")
def db_connection():
    """Provides an active database connection for tests."""
    conn = sqlite3.connect(DATABASE_FILE)
    init_db(conn)
    yield conn
    conn.close()


@pytest.fixture(scope="session")
def sample_documents_dir():
    """Returns the documents directory."""
    return DOCUMENTS_DIR
