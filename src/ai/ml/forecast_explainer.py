"""
Forecast Explainer for InsightAI ML Agent

Generates business-oriented interpretations of ML revenue forecasts,
transparently discussing model accuracy metrics (MAE, RMSE, R²),
uncertainty bounds, and operational assumptions.
"""

from typing import Dict, Any, Optional
import pandas as pd
from src.llm.llm_service import ask_llm


ML_EXPLAINER_SYSTEM_PROMPT = """
You are a senior business intelligence and forecasting specialist for InsightAI.
Your role is to explain machine learning revenue forecasts clearly and objectively.

CRITICAL GUIDELINES:
1. Explain the historical revenue trend clearly.
2. Ground explanations in the actual numbers and model evaluation metrics provided.
3. Explicitly state prediction uncertainty and key operational limitations (e.g. macro market shifts, seasonal shocks).
4. Never present statistical predictions as guaranteed facts.
5. Provide 1-2 actionable commercial recommendations based on the forecast.
6. Keep the response professional, concise, and executive-ready (under 160 words).
"""


def explain_forecast(
    historical_data: pd.DataFrame,
    predicted_revenue: float,
    model_name: str = "Linear Regression",
    mae: Optional[float] = None,
    rmse: Optional[float] = None,
    r2: Optional[float] = None,
    lower_bound: Optional[float] = None,
    upper_bound: Optional[float] = None,
) -> str:
    """
    Generate a comprehensive business explanation for the ML forecast.
    """
    revenue_series = historical_data["total_revenue"].tolist()
    recent_revenues = [f"₹{r:,.0f}" for r in revenue_series[-6:]]

    metrics_text = ""
    if mae is not None and rmse is not None and r2 is not None:
        metrics_text = f"""
Model Architecture: {model_name}
Model Evaluation Metrics:
- MAE (Mean Absolute Error): ₹{mae:,.2f}
- RMSE (Root Mean Squared Error): ₹{rmse:,.2f}
- R² Score: {r2:.3f}
"""

    uncertainty_text = ""
    if lower_bound is not None and upper_bound is not None:
        uncertainty_text = f"Projected Range: ₹{lower_bound:,.2f} to ₹{upper_bound:,.2f} (80% Confidence Interval)"

    prompt = f"""
Recent Historical Monthly Revenues:
{recent_revenues}

Forecasted Revenue for Next Period:
₹{predicted_revenue:,.2f}

{metrics_text}
{uncertainty_text}

Provide:
1. Trend trajectory & underlying growth/stability factors.
2. Forecast explanation with evaluation confidence.
3. Risks, uncertainty factors, and operational recommendations.
"""
    return ask_llm(
        prompt=prompt,
        system_prompt=ML_EXPLAINER_SYSTEM_PROMPT,
        max_tokens=300,
        temperature=0.2,
    )
