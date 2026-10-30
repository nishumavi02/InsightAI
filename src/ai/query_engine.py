"""
Query Engine

High-level interface for querying InsightAI from the Streamlit UI and external APIs.
Connects directly to the Agent Orchestrator while maintaining conversation memory.
"""

import sqlite3
from typing import Optional, List, Dict, Any

from src.ai.agent_orchestrator import orchestrate, run_agent


def process_question_with_router(
    question: str,
    connection: sqlite3.Connection,
    chunks: Optional[List[str]] = None,
    chunk_embeddings: Optional[Any] = None,
    conversation_history: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Process a natural language business question through the intelligent orchestrator.
    Returns the comprehensive synthesized response object.
    """
    return orchestrate(
        question=question,
        connection=connection,
        chunks=chunks,
        chunk_embeddings=chunk_embeddings,
        conversation_history=conversation_history,
    )


def process_question(question: str, connection: sqlite3.Connection) -> str:
    """
    Legacy convenience helper that routes a question and returns plain text answer.
    """
    res = orchestrate(question=question, connection=connection)
    return res["answer"]
