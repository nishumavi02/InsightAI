"""
AI Service for InsightAI

Generates executive business intelligence summaries, business health diagnostics,
and strategic recommendations from verified enterprise data.
"""

import sqlite3
from typing import Dict, Any, Tuple

from src.ai.business_context import build_business_context
from src.ai.executive_summary import generate_executive_summary


def calculate_business_status(context: Dict[str, Any]) -> str:
    """Determine overall business health."""
    revenue = context.get("total_revenue", 0)
    orders = context.get("total_orders", 0)

    if revenue > 50000 and orders > 100:
        return "Healthy"
    if revenue > 25000:
        return "Stable"
    if revenue > 10000:
        return "Needs Attention"
    return "Critical"


def calculate_ai_confidence(context: Dict[str, Any]) -> Tuple[int, str]:
    """Dynamically assess AI confidence based on data completeness."""
    revenue = context.get("total_revenue", 0)
    orders = context.get("total_orders", 0)
    customers = context.get("total_customers", 0)

    if revenue > 0 and orders > 50 and customers > 20:
        score = 95
        explanation = "High confidence: Summary is grounded in verified transactional records with robust sample size."
    elif revenue > 0 and orders > 0:
        score = 80
        explanation = "Moderate confidence: Analysis supported by database records with limited transaction history."
    else:
        score = 45
        explanation = "Low confidence: Limited or missing business transaction data."

    return score, explanation


def get_ai_executive_summary(connection: sqlite3.Connection) -> Dict[str, Any]:
    """Generate complete AI Executive Summary."""
    context = build_business_context(connection)
    summary = generate_executive_summary(context)
    status = calculate_business_status(context)
    confidence, explanation = calculate_ai_confidence(context)

    return {
        "status": status,
        "confidence": confidence,
        "confidence_reason": explanation,
        "summary": summary,
    }
