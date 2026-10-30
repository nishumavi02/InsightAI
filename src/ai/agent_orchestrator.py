"""
Agent Orchestrator

Coordinates the Decision Router, specialized AI Agents (SQL, RAG, ML),
and the AI Reasoning Layer to deliver grounded business decision intelligence.
"""

import sqlite3
from typing import Union, Dict, Any, Optional, List

from src.ai.decision_router import route_question_with_metadata
from src.ai.sql_agent import run_sql_agent
from src.ai.rag.rag_agent import run_rag_agent
from src.ai.ml.ml_agent import run_ml_agent
from src.ai.reasoning_layer import synthesize_agent_response


def orchestrate(
    question: str,
    connection: sqlite3.Connection,
    chunks: Optional[List[str]] = None,
    chunk_embeddings: Optional[Any] = None,
    conversation_history: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    End-to-end intelligent execution pipeline:
    User Question
    -> Contextual Decision Router
    -> Specialized Agent Execution (SQL / RAG / ML)
    -> AI Reasoning Layer
    -> Unified Synthesized Business Response
    """
    # Step 1: Context-aware routing
    route_info = route_question_with_metadata(question, conversation_history)
    selected_agent = route_info["route"]

    # Step 2: Dispatch to appropriate agent
    raw_agent_result = None

    if selected_agent == "SQL":
        raw_agent_result = run_sql_agent(
            question=question,
            connection=connection,
            return_dict=True,
        )

    elif selected_agent == "RAG":
        raw_agent_result = run_rag_agent(
            question=question,
            chunks=chunks,
            chunk_embeddings=chunk_embeddings,
            return_dict=True,
        )

    elif selected_agent == "ML":
        raw_agent_result = run_ml_agent(
            connection=connection,
            question=question,
        )

    # Step 3: AI Reasoning Layer synthesis
    response = synthesize_agent_response(
        question=question,
        route_info=route_info,
        raw_agent_result=raw_agent_result,
        conversation_history=conversation_history,
    )

    return response


def run_agent(
    question: str,
    connection: sqlite3.Connection,
    chunks: Optional[List[str]] = None,
    chunk_embeddings: Optional[Any] = None,
    return_full_response: bool = False,
) -> Union[str, Dict[str, Any]]:
    """
    Route a question to the appropriate agent and return its answer.
    Preserves exact backward compatibility with test suites while supporting
    new full response synthesis.
    """
    route_info = route_question_with_metadata(question)
    route = route_info["route"]

    print(f"\n--- ROUTED AGENT: {route} ---")

    if return_full_response:
        return orchestrate(
            question=question,
            connection=connection,
            chunks=chunks,
            chunk_embeddings=chunk_embeddings,
        )

    if route == "SQL":
        return run_sql_agent(
            question=question,
            connection=connection,
            return_dict=False,
        )

    elif route == "RAG":
        return run_rag_agent(
            question=question,
            chunks=chunks,
            chunk_embeddings=chunk_embeddings,
            return_dict=False,
        )

    elif route == "ML":
        return run_ml_agent(
            connection=connection,
            question=question,
        )

    return (
        "Sorry, I could not determine "
        "which agent should handle this question."
    )
