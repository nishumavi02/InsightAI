"""
Decision Router for InsightAI

Routes user queries to the appropriate specialized agent (SQL, RAG, ML)
using contextual classification with high-accuracy heuristic fallbacks.
"""

import re
from typing import Dict, Any, Optional, List


def classify_intent_heuristics(question: str) -> Dict[str, Any]:
    """
    High-confidence rule-based classification for fast, deterministic routing.
    """
    q = question.lower().strip()

    # ML Forecasting Keywords
    ml_patterns = [
        r"\bpredict\b", r"\bprediction\b", r"\bpredictions\b",
        r"\bforecast\b", r"\bforecasting\b", r"\bforecasts\b",
        r"\bfuture revenue\b", r"\bfuture sales\b", r"\bnext month\b",
        r"\bnext quarter\b", r"\bnext year\b", r"\bprojection\b",
        r"\bprojections\b", r"\btrend forecast\b", r"\bmachine learning\b",
    ]
    for pattern in ml_patterns:
        if re.search(pattern, q):
            return {
                "route": "ML",
                "confidence": 0.95,
                "reason": f"Query contains predictive intent matched by pattern '{pattern}'.",
            }

    # RAG Document Keywords
    rag_patterns = [
        r"\bpolicy\b", r"\bpolicies\b", r"\bleave\b", r"\bleaves\b",
        r"\bvacation\b", r"\bholiday\b", r"\bholidays\b",
        r"\bguideline\b", r"\bguidelines\b", r"\brules\b",
        r"\bremote work\b", r"\bwork from home\b", r"\bwfh\b",
        r"\bhandbook\b", r"\bemployee\b", r"\bemployees\b",
        r"\bhr\b", r"\bcarry forward\b", r"\bworking days\b",
        r"\bworking hours\b", r"\bappraisal\b", r"\bperformance review\b",
        r"\bnotice period\b", r"\bbenefits\b", r"\bmaternity\b", r"\bpaternity\b",
    ]
    for pattern in rag_patterns:
        if re.search(pattern, q):
            return {
                "route": "RAG",
                "confidence": 0.95,
                "reason": f"Query references internal company policy/documentation via '{pattern}'.",
            }

    # SQL Analytics (Structured Database queries)
    sql_patterns = [
        r"\brevenue\b", r"\bsales\b", r"\bcost\b", r"\bprice\b",
        r"\border\b", r"\borders\b", r"\bcustomer\b", r"\bcustomers\b",
        r"\bproduct\b", r"\bproducts\b", r"\bcategory\b", r"\bcategories\b",
        r"\bcity\b", r"\bcities\b", r"\bstate\b", r"\bstates\b",
        r"\btop\b", r"\bhighest\b", r"\blowest\b", r"\bbottom\b",
        r"\baverage\b", r"\btotal\b", r"\bcount\b", r"\bhow many\b",
        r"\bwho spent\b", r"\bmost expensive\b", r"\bquantity\b",
    ]
    for pattern in sql_patterns:
        if re.search(pattern, q):
            return {
                "route": "SQL",
                "confidence": 0.90,
                "reason": f"Query requests structured transactional metrics matching '{pattern}'.",
            }

    # Default route for general business questions
    return {
        "route": "SQL",
        "confidence": 0.70,
        "reason": "Defaulting to SQL analytical engine for general business query.",
    }


def route_question(question: str) -> str:
    """
    Decide which agent should answer the question.
    Preserves exact backward compatibility with test_decision_router.py.
    """
    res = classify_intent_heuristics(question)
    return res["route"]


def route_question_with_metadata(
    question: str,
    conversation_history: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Context-aware routing returning the selected agent, confidence, and reasoning.
    Does NOT prepend historical text to question to prevent false keyword triggers.
    """
    # Check if this is a pronoun follow-up referring to an earlier entity
    q_lower = question.lower().strip()
    is_follow_up = bool(re.search(r"\b(it|they|them|he|she|this|that|those|these)\b", q_lower))

    base_routing = classify_intent_heuristics(question)

    if is_follow_up and conversation_history and len(conversation_history) > 0:
        last_turn = conversation_history[-1]
        last_agent = last_turn.get("agent_used") or classify_intent_heuristics(last_turn.get("question", ""))["route"]
        # If current question has low confidence, inherit route from previous turn
        if base_routing["confidence"] <= 0.70:
            return {
                "route": last_agent,
                "confidence": 0.85,
                "reason": f"Follow-up query refers to previous conversation context handled by {last_agent}.",
                "is_follow_up": True,
            }

    base_routing["is_follow_up"] = False
    return base_routing
