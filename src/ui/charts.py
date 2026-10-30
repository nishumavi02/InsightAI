"""
Charts UI Component for InsightAI

Renders interactive Plotly visual analytics with theme-adaptive styling
that seamlessly works in Light, Dark, and System themes.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from src.analytics.analytics_service import (
    get_top_products,
    get_top_customers,
    get_revenue_by_category,
    get_revenue_by_city,
    get_monthly_revenue_trend,
)


def render_revenue_trend_chart(connection):
    """Render monthly revenue trend with moving average."""
    trend_df = get_monthly_revenue_trend(connection)
    if trend_df.empty:
        st.info("No historical revenue trend data available.")
        return

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=trend_df["month"],
        y=trend_df["total_revenue"],
        name="Monthly Revenue",
        marker_color="#3B82F6",
        opacity=0.85,
        hovertemplate="%{x}<br>Revenue: Rs. %{y:,.2f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=trend_df["month"],
        y=trend_df["total_revenue"],
        mode="lines+markers",
        name="Trend Line",
        line=dict(color="#10B981", width=3),
        marker=dict(size=7, color="#059669"),
        hovertemplate="Trend: Rs. %{y:,.2f}<extra></extra>",
    ))

    fig.update_layout(
        title={"text": "<b>Monthly Revenue Trajectory</b>", "x": 0.02, "font": {"size": 17}},
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Month",
        yaxis_title="Revenue (Rs.)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")


def render_category_revenue_chart(connection):
    """Render category breakdown horizontal bar chart."""
    cat_df = get_revenue_by_category(connection)
    if cat_df.empty:
        st.info("No category data available.")
        return

    fig = px.bar(
        cat_df,
        x="total_revenue",
        y="category",
        orientation="h",
        text="total_revenue",
        color="total_revenue",
        color_continuous_scale="Blues",
    )
    fig.update_traces(
        texttemplate="Rs. %{text:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Revenue: Rs. %{x:,.2f}<extra></extra>",
    )
    fig.update_layout(
        title={"text": "<b>Revenue by Product Category</b>", "x": 0.02, "font": {"size": 17}},
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        xaxis_title="Revenue (Rs.)",
        yaxis_title="Category",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=20, r=20, t=50, b=20),
    )
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")


def render_city_revenue_chart(connection):
    """Render city sales bar chart."""
    city_df = get_revenue_by_city(connection, limit=10)
    if city_df.empty:
        st.info("No city data available.")
        return

    fig = px.bar(
        city_df,
        x="city",
        y="total_revenue",
        text="total_revenue",
        color="total_revenue",
        color_continuous_scale="Purples",
    )
    fig.update_traces(
        texttemplate="Rs. %{text:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{x}</b> (%{customdata})<br>Revenue: Rs. %{y:,.2f}<extra></extra>",
        customdata=city_df["state"],
    )
    fig.update_layout(
        title={"text": "<b>Top 10 Cities by Revenue</b>", "x": 0.02, "font": {"size": 17}},
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        xaxis_title="City",
        yaxis_title="Revenue (Rs.)",
        margin=dict(l=20, r=20, t=50, b=20),
    )
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")


def render_customer_spending_chart(connection):
    """Render top customer spending bar chart."""
    cust_df = get_top_customers(connection, limit=10)
    if cust_df.empty:
        st.info("No customer data available.")
        return

    fig = px.bar(
        cust_df,
        x="total_spent",
        y="customer_name",
        orientation="h",
        text="total_spent",
        color="total_spent",
        color_continuous_scale="Teal",
    )
    fig.update_traces(
        texttemplate="Rs. %{text:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b> (%{customdata})<br>Total Spent: Rs. %{x:,.2f}<extra></extra>",
        customdata=cust_df["city"],
    )
    fig.update_layout(
        title={"text": "<b>Top 10 Customers by Total Spending</b>", "x": 0.02, "font": {"size": 17}},
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        xaxis_title="Total Spent (Rs.)",
        yaxis_title="Customer",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=20, r=20, t=50, b=20),
    )
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")


def render_sales_analytics(connection):
    """
    Render all primary sales analytics components.
    Preserves exact backward compatibility with existing tests and dashboard.
    """
    st.markdown("### 📈 Revenue & Market Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        render_revenue_trend_chart(connection)
    with col2:
        render_category_revenue_chart(connection)

    col3, col4 = st.columns(2)
    with col3:
        render_city_revenue_chart(connection)
    with col4:
        render_customer_spending_chart(connection)

    st.markdown("### 📦 Product Performance Table")
    products_df = get_top_products(connection, limit=15)
    st.dataframe(
        products_df.style.format({
            "price": "Rs. {:,.2f}",
            "units_sold": "{:,}",
            "total_revenue": "Rs. {:,.2f}",
        }),
        use_container_width=True,
        height=320,
    )
