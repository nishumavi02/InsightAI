"""
Forecast Chart UI Component for InsightAI

Renders advanced forecasting visualizations with confidence intervals,
historical trend comparison, and model evaluation metrics across all themes.
"""

from typing import Optional, List, Dict, Any
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_forecast_chart(
    historical_data: pd.DataFrame,
    predicted_revenue: float,
    future_projections: Optional[List[Dict[str, Any]]] = None,
    best_model_name: Optional[str] = None,
    mae: Optional[float] = None,
    rmse: Optional[float] = None,
    r2: Optional[float] = None,
    comparison_table: Optional[pd.DataFrame] = None,
):
    """
    Render comprehensive revenue forecast chart with historical actuals,
    projected periods, and confidence intervals. Adapts to Light, Dark, and System themes.
    """
    hist_df = historical_data.copy()
    hist_df["month_str"] = pd.to_datetime(hist_df["month"]).dt.strftime("%Y-%m")

    fig = go.Figure()

    # 1. Historical Actuals Line
    fig.add_trace(go.Scatter(
        x=hist_df["month_str"],
        y=hist_df["total_revenue"],
        mode="lines+markers",
        name="Historical Revenue (Actual)",
        line=dict(color="#3B82F6", width=3),
        marker=dict(size=7, color="#1D4ED8"),
        hovertemplate="Actual: Rs. %{y:,.2f}<br>Month: %{x}<extra></extra>",
    ))

    # 2. Build future forecast points
    if future_projections and len(future_projections) > 0:
        future_months = [p["month"] for p in future_projections]
        future_preds = [p["predicted_revenue"] for p in future_projections]
        upper_bounds = [p.get("upper_bound", p["predicted_revenue"] * 1.1) for p in future_projections]
        lower_bounds = [p.get("lower_bound", p["predicted_revenue"] * 0.9) for p in future_projections]
    else:
        # Default single next month projection
        last_dt = pd.to_datetime(hist_df["month"].iloc[-1])
        next_dt_str = (last_dt + pd.DateOffset(months=1)).strftime("%Y-%m")
        future_months = [next_dt_str]
        future_preds = [predicted_revenue]
        upper_bounds = [predicted_revenue * 1.08]
        lower_bounds = [predicted_revenue * 0.92]

    # Connect the last historical point with the first forecast point
    bridge_x = [hist_df["month_str"].iloc[-1]] + future_months
    bridge_y = [hist_df["total_revenue"].iloc[-1]] + future_preds
    bridge_upper = [hist_df["total_revenue"].iloc[-1]] + upper_bounds
    bridge_lower = [hist_df["total_revenue"].iloc[-1]] + lower_bounds

    # 3. Upper Bound (Shaded Confidence Area boundary)
    fig.add_trace(go.Scatter(
        x=bridge_x,
        y=bridge_upper,
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip",
    ))

    # 4. Lower Bound (Fills to Upper Bound)
    fig.add_trace(go.Scatter(
        x=bridge_x,
        y=bridge_lower,
        mode="lines",
        line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(245, 158, 11, 0.20)",
        name="80% Confidence Interval",
        hovertemplate="Range: Rs. %{y:,.2f}<extra></extra>",
    ))

    # 5. Projected Revenue Line (Dashed Amber)
    fig.add_trace(go.Scatter(
        x=bridge_x,
        y=bridge_y,
        mode="lines+markers",
        name="ML Projected Revenue",
        line=dict(color="#F59E0B", width=3, dash="dash"),
        marker=dict(size=8, color="#D97706", symbol="diamond"),
        hovertemplate="Projected: Rs. %{y:,.2f}<br>Month: %{x}<extra></extra>",
    ))

    fig.update_layout(
        title={
            "text": "<b>Historical vs. Machine Learning Forecast Trajectory</b>",
            "x": 0.02,
            "font": {"size": 17},
        },
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Month",
        yaxis_title="Revenue (Rs.)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

    # Display Model Evaluation Metrics if provided
    if mae is not None and rmse is not None and r2 is not None:
        st.markdown("#### 🎯 Model Evaluation Metrics")
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.metric("Selected Algorithm", best_model_name or "Best Fit")
        with m_col2:
            st.metric("MAE (Mean Absolute Error)", f"Rs. {mae:,.2f}")
        with m_col3:
            st.metric("RMSE", f"Rs. {rmse:,.2f}")
        with m_col4:
            st.metric("R² Score", f"{r2:.3f}")

    # Display Model Comparison Table if provided
    if comparison_table is not None and not comparison_table.empty:
        with st.expander("📊 View Model Comparison Benchmarks (Candidate Algorithms)", expanded=False):
            st.dataframe(
                comparison_table[["model_name", "mae", "rmse", "r2", "selected"]].rename(
                    columns={
                        "model_name": "Algorithm",
                        "mae": "MAE (Rs.)",
                        "rmse": "RMSE (Rs.)",
                        "r2": "R²",
                        "selected": "Selected as Best",
                    }
                ),
                use_container_width=True,
            )
