"""
Unit tests for InsightAI ML Agent & Revenue Forecasting.
"""

import pytest
import pandas as pd

from src.ai.ml.ml_data_service import get_monthly_revenue
from src.ai.ml.forecasting_service import forecast_revenue, train_and_compare_models
from src.ai.ml.ml_agent import run_ml_agent


def test_get_monthly_revenue(db_connection):
    monthly_df = get_monthly_revenue(db_connection)
    assert isinstance(monthly_df, pd.DataFrame)
    assert len(monthly_df) == 12
    assert "month" in monthly_df.columns
    assert "total_revenue" in monthly_df.columns


def test_model_comparison_and_evaluation(db_connection):
    monthly_df = get_monthly_revenue(db_connection)
    model_info, comp_df = train_and_compare_models(monthly_df)

    assert "best_model_name" in model_info
    assert "mae" in model_info
    assert "rmse" in model_info
    assert "r2" in model_info
    assert model_info["mae"] > 0
    assert model_info["rmse"] > 0

    assert len(comp_df) >= 3
    assert set(["Linear Regression", "Ridge Regression", "Random Forest"]).issubset(set(comp_df["model_name"]))


def test_forecast_multi_horizon(db_connection):
    monthly_df = get_monthly_revenue(db_connection)
    res = forecast_revenue(monthly_df, horizon_months=3)

    assert res["predicted_revenue"] > 0
    assert len(res["future_projections"]) == 3
    for proj in res["future_projections"]:
        assert "month" in proj
        assert "predicted_revenue" in proj
        assert "lower_bound" in proj
        assert "upper_bound" in proj
        assert proj["lower_bound"] <= proj["predicted_revenue"] <= proj["upper_bound"]


def test_run_ml_agent_execution(db_connection):
    res = run_ml_agent(db_connection, question="Predict next quarter revenue")
    assert isinstance(res, dict)
    assert res["agent"] == "ML"
    assert "predicted_revenue" in res
    assert "forecast_explanation" in res
    assert "comparison_table" in res
