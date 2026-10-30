"""
AI Reasoning Layer for InsightAI

Synthesizes agent outputs, computes holistic confidence scores,
validates output grounding, and generates context-aware follow-up suggestions.
"""

from typing import Dict, Any, List, Optional
import pandas as pd


def generate_follow_up_suggestions(
    agent: str,
    question: str,
    raw_result: Any,
) -> List[str]:
    """
    Generate 2-3 logical follow-up questions based on the agent and current result.
    """
    q = question.lower()

    if agent == "SQL":
        if "category" in q:
            return [
                "Which city generates the highest revenue for this category?",
                "What are the top 5 best-selling products in this category?",
                "Predict next month's revenue for this category",
            ]
        if "customer" in q:
            return [
                "What products does this customer purchase most often?",
                "Which city has the largest customer base?",
                "What is our average customer lifetime spend?",
            ]
        if "city" in q:
            return [
                "Which product category performs best in this city?",
                "Who is the top-spending customer in this city?",
                "How does this city's revenue compare to the national average?",
            ]
        if "revenue" in q or "sales" in q:
            return [
                "Predict revenue for the next 3 months",
                "Which product category contributed the most revenue?",
                "What is the average spending per customer?",
            ]
        return [
            "What is our total revenue across all categories?",
            "Who are our top 5 revenue-generating customers?",
            "Can employees work remotely according to company policy?",
        ]

    elif agent == "RAG":
        if "leave" in q or "vacation" in q:
            return [
                "Can unused leave be carried forward to next year?",
                "How many days in advance must leave requests be submitted?",
                "What is the company remote work policy?",
            ]
        if "remote" in q or "work from home" in q:
            return [
                "Does remote work require manager approval?",
                "How many paid leave days are employees entitled to?",
                "What are the standard office working days?",
            ]
        return [
            "How many paid leave days do employees receive per year?",
            "What is the company policy on remote work?",
            "What were our total sales last month?",
        ]

    elif agent == "ML":
        return [
            "What was the actual historical revenue trend over the past 6 months?",
            "Which model had the lowest error (RMSE) during evaluation?",
            "Which product category is expected to drive the most growth?",
        ]

    return [
        "What is total revenue for the year?",
        "Which product is our top seller?",
        "What is company policy regarding employee leave?",
    ]


def synthesize_agent_response(
    question: str,
    route_info: Dict[str, Any],
    raw_agent_result: Any,
    conversation_history: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Synthesize raw agent output into a unified, high-integrity response contract.
    """
    agent = route_info.get("route", "SQL")
    routing_confidence = route_info.get("confidence", 0.9)

    # 1. Normalize fields based on agent return type
    answer = ""
    sql_query = None
    data_df = None
    sources = []
    forecast_meta = {}
    agent_confidence = 0.90
    status = "success"

    if agent == "SQL":
        if isinstance(raw_agent_result, dict):
            answer = raw_agent_result.get("answer", "")
            sql_query = raw_agent_result.get("sql_query")
            data_df = raw_agent_result.get("data")
            agent_confidence = raw_agent_result.get("confidence", 0.95)
            if raw_agent_result.get("error"):
                status = "error"
        else:
            answer = str(raw_agent_result)
            if "failed" in answer.lower() or "error" in answer.lower():
                status = "warning"
                agent_confidence = 0.3

    elif agent == "RAG":
        if isinstance(raw_agent_result, dict):
            answer = raw_agent_result.get("answer", "")
            sources = raw_agent_result.get("sources", [])
            agent_confidence = raw_agent_result.get("confidence", 0.85)
            if not raw_agent_result.get("is_grounded", True):
                status = "warning"
        else:
            answer = str(raw_agent_result)
            sources = ["company_policy.txt"]
            if "not contain" in answer.lower() or "insufficient" in answer.lower():
                status = "warning"
                agent_confidence = 0.40

    elif agent == "ML":
        if isinstance(raw_agent_result, dict):
            answer = raw_agent_result.get("answer", "")
            data_df = raw_agent_result.get("historical_data")
            forecast_meta = {
                "predicted_revenue": raw_agent_result.get("predicted_revenue"),
                "best_model_name": raw_agent_result.get("best_model_name"),
                "mae": raw_agent_result.get("mae"),
                "rmse": raw_agent_result.get("rmse"),
                "r2": raw_agent_result.get("r2"),
                "future_projections": raw_agent_result.get("future_projections", []),
                "comparison_table": raw_agent_result.get("comparison_table"),
                "forecast_explanation": raw_agent_result.get("forecast_explanation", ""),
            }
            agent_confidence = raw_agent_result.get("confidence", 0.80)
        else:
            answer = str(raw_agent_result)

    # 2. Overall confidence calculation
    overall_confidence = round(routing_confidence * agent_confidence, 2)

    # 3. Generate proactive follow-up suggestions
    follow_ups = generate_follow_up_suggestions(agent, question, raw_agent_result)

    return {
        "agent": agent,
        "question": question,
        "answer": answer,
        "confidence": overall_confidence,
        "routing_reason": route_info.get("reason", ""),
        "status": status,
        "sql_query": sql_query,
        "data": data_df,
        "sources": sources,
        "forecast_meta": forecast_meta,
        "follow_ups": follow_ups,
    }
