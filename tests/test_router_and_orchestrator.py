"""
Unit tests for Decision Router, AI Reasoning Layer, and Agent Orchestrator.
"""

import pytest

from src.ai.decision_router import route_question, route_question_with_metadata
from src.ai.agent_orchestrator import orchestrate, run_agent
from src.ai.reasoning_layer import synthesize_agent_response, generate_follow_up_suggestions


def test_decision_router_intent_selection():
    assert route_question("Predict revenue for next month") == "ML"
    assert route_question("What is the company leave policy?") == "RAG"
    assert route_question("Which product generated highest sales?") == "SQL"
    assert route_question("What is our total revenue?") == "SQL"


def test_routing_prevents_keyword_pollution():
    # Context with past RAG question shouldn't corrupt current SQL question
    history = [
        {"question": "What is the policy for sick leave?", "answer": "18 days", "agent_used": "RAG"}
    ]
    meta = route_question_with_metadata("What is our total revenue?", conversation_history=history)
    assert meta["route"] == "SQL"


def test_reasoning_layer_follow_up_generation():
    follow_ups = generate_follow_up_suggestions("SQL", "Which category has highest revenue?", {})
    assert len(follow_ups) >= 2

    ml_follow_ups = generate_follow_up_suggestions("ML", "Predict sales", {})
    assert len(ml_follow_ups) >= 2


def test_orchestrator_end_to_end(db_connection):
    resp = orchestrate("What is our total revenue?", db_connection)
    assert isinstance(resp, dict)
    assert resp["agent"] == "SQL"
    assert "answer" in resp
    assert "follow_ups" in resp
    assert len(resp["follow_ups"]) >= 2
    assert resp["confidence"] > 0.5
