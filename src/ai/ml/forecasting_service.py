"""
Forecasting utilities for InsightAI.

Provides multi-model revenue forecasting with evaluation metrics (MAE, RMSE, R²),
model comparison, confidence intervals, and uncertainty quantification.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


def _calc_rmse(y_true, y_pred) -> float:
    """Calculate Root Mean Squared Error."""
    return float(np.sqrt(np.mean((np.array(y_true) - np.array(y_pred)) ** 2)))


def train_and_compare_models(monthly_df: pd.DataFrame) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """
    Train multiple candidate models on historical revenue data, evaluate their
    performance using MAE, RMSE, and R², and select the best model.
    """
    df = monthly_df.copy().reset_index(drop=True)
    n_samples = len(df)

    if n_samples < 3:
        raise ValueError("At least 3 monthly data points are required for forecasting.")

    # Feature engineering
    df["month_index"] = np.arange(n_samples)
    X = df[["month_index"]].values
    y = df["total_revenue"].values

    # Determine train/test split: use last 20% (min 1 sample) for validation if n >= 5
    if n_samples >= 5:
        split_idx = max(int(n_samples * 0.75), n_samples - 2)
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
    else:
        # If very few points, train and evaluate on whole set with sample penalty
        X_train, X_val = X, X
        y_train, y_val = y, y

    candidate_models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
        "Random Forest": RandomForestRegressor(n_estimators=50, random_state=42, max_depth=3),
    }

    results = []
    trained_instances = {}

    for name, model in candidate_models.items():
        model.fit(X_train, y_train)
        preds_val = model.predict(X_val)

        mae = float(mean_absolute_error(y_val, preds_val))
        rmse = _calc_rmse(y_val, preds_val)
        
        # Calculate R² (guard against negative or zero variance)
        try:
            r2 = float(r2_score(y_val, preds_val))
            if np.isnan(r2) or np.isinf(r2):
                r2 = 0.0
        except Exception:
            r2 = 0.0

        # Refit on entire dataset for future projection
        model.fit(X, y)
        trained_instances[name] = model

        results.append({
            "model_name": name,
            "mae": round(mae, 2),
            "rmse": round(rmse, 2),
            "r2": round(r2, 3),
            "rmse_raw": rmse,
        })

    comparison_df = pd.DataFrame(results)

    # Best model has lowest validation RMSE
    best_row = comparison_df.sort_values(by="rmse_raw", ascending=True).iloc[0]
    best_model_name = best_row["model_name"]
    best_model = trained_instances[best_model_name]

    # Calculate residuals for uncertainty estimation
    full_preds = best_model.predict(X)
    residuals = y - full_preds
    residual_std = float(np.std(residuals)) if len(residuals) > 1 else float(0.1 * np.mean(y))

    comparison_df["selected"] = comparison_df["model_name"] == best_model_name

    model_info = {
        "best_model_name": best_model_name,
        "best_model": best_model,
        "mae": best_row["mae"],
        "rmse": best_row["rmse"],
        "r2": best_row["r2"],
        "residual_std": residual_std,
        "historical_data": df,
        "trained_models": trained_instances,
    }

    return model_info, comparison_df


def forecast_revenue(
    monthly_revenue_df: pd.DataFrame,
    horizon_months: int = 3,
) -> Dict[str, Any]:
    """
    Generate revenue forecasts for future months with confidence intervals.
    """
    model_info, comparison_df = train_and_compare_models(monthly_revenue_df)
    df = model_info["historical_data"]
    best_model = model_info["best_model"]
    residual_std = model_info["residual_std"]

    n_samples = len(df)
    last_date = pd.to_datetime(df["month"].iloc[-1])

    future_projections = []
    future_indices = np.arange(n_samples, n_samples + horizon_months).reshape(-1, 1)
    raw_predictions = best_model.predict(future_indices)

    for i, pred in enumerate(raw_predictions):
        future_month = last_date + pd.DateOffset(months=i + 1)
        pred_val = max(float(pred), 0.0)
        # 80% confidence interval ~ 1.28 * std
        uncertainty = 1.28 * residual_std * np.sqrt(1 + (i + 1) * 0.15)
        lower_bound = max(pred_val - uncertainty, 0.0)
        upper_bound = pred_val + uncertainty

        future_projections.append({
            "month": future_month.strftime("%Y-%m"),
            "predicted_revenue": round(pred_val, 2),
            "lower_bound": round(lower_bound, 2),
            "upper_bound": round(upper_bound, 2),
        })

    next_month_pred = future_projections[0]["predicted_revenue"]

    return {
        "predicted_revenue": next_month_pred,
        "training_points": n_samples,
        "historical_data": df,
        "best_model_name": model_info["best_model_name"],
        "mae": model_info["mae"],
        "rmse": model_info["rmse"],
        "r2": model_info["r2"],
        "future_projections": future_projections,
        "comparison_table": comparison_df,
    }


def forecast_next_month(monthly_revenue_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Predict next month's revenue while providing full model evaluation metrics.
    Preserves exact backward compatibility with test_forecasting.py.
    """
    res = forecast_revenue(monthly_revenue_df, horizon_months=1)
    return {
        "predicted_revenue": res["predicted_revenue"],
        "training_points": res["training_points"],
        "historical_data": res["historical_data"],
        "mae": res["mae"],
        "rmse": res["rmse"],
        "r2": res["r2"],
        "best_model_name": res["best_model_name"],
        "future_projections": res["future_projections"],
        "comparison_table": res["comparison_table"],
    }
