"""
ML Agent

Responsible for handling predictive analytics and revenue forecasting
with model evaluation, comparison, and uncertainty explanation.
"""

import sqlite3
from typing import Dict, Any, Optional

from src.ai.ml.ml_data_service import get_monthly_revenue
from src.ai.ml.forecasting_service import forecast_revenue
from src.ai.ml.forecast_explainer import explain_forecast


def run_ml_agent(
    connection: sqlite3.Connection,
    question: Optional[str] = None,
    horizon_months: int = 3,
) -> Dict[str, Any]:
    """
    Execute the ML forecasting pipeline:
    1. Retrieve aggregated monthly revenue from database
    2. Train and evaluate multiple candidate models (Linear, Ridge, Random Forest)
    3. Calculate evaluation metrics (MAE, RMSE, R²)
    4. Project future revenue across forecast horizon with uncertainty bounds
    5. Generate executive-level explanation and recommendation
    """
    monthly_revenue = get_monthly_revenue(connection)

    # If user question mentions specific months, parse horizon if present
    if question:
        q_lower = question.lower()
        if "6 month" in q_lower or "six month" in q_lower:
            horizon_months = 6
        elif "1 month" in q_lower or "next month" in q_lower:
            horizon_months = 1
        elif "year" in q_lower or "12 month" in q_lower:
            horizon_months = 12

    forecast_res = forecast_revenue(monthly_revenue, horizon_months=horizon_months)

    predicted_revenue = forecast_res["predicted_revenue"]
    historical_data = forecast_res["historical_data"]
    training_points = forecast_res["training_points"]
    best_model_name = forecast_res["best_model_name"]
    mae = forecast_res["mae"]
    rmse = forecast_res["rmse"]
    r2 = forecast_res["r2"]
    future_projections = forecast_res["future_projections"]
    comparison_table = forecast_res["comparison_table"]

    # First future period interval
    first_proj = future_projections[0] if future_projections else {}
    lower_bound = first_proj.get("lower_bound", predicted_revenue * 0.9)
    upper_bound = first_proj.get("upper_bound", predicted_revenue * 1.1)

    forecast_explanation = explain_forecast(
        historical_data=historical_data,
        predicted_revenue=predicted_revenue,
        model_name=best_model_name,
        mae=mae,
        rmse=rmse,
        r2=r2,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
    )

    answer = (
        f"Based on {training_points} months of historical sales data evaluated using "
        f"{best_model_name} (MAE: Rs. {mae:,.0f}, RMSE: Rs. {rmse:,.0f}, R2: {r2:.2f}), "
        f"projected revenue for next month is approximately Rs. {predicted_revenue:,.2f} "
        f"(expected range: Rs. {lower_bound:,.2f} - Rs. {upper_bound:,.2f})."
    )

    return {
        "agent": "ML",
        "answer": answer,
        "historical_data": historical_data,
        "predicted_revenue": predicted_revenue,
        "forecast_explanation": forecast_explanation,
        "training_points": training_points,
        "best_model_name": best_model_name,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "future_projections": future_projections,
        "comparison_table": comparison_table,
        "confidence": round(max(min(float(r2), 0.95), 0.50), 2) if r2 > 0 else 0.70,
    }
