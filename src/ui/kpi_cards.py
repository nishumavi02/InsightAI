"""
KPI Cards UI Component for InsightAI

Renders high-impact executive KPI metrics with theme-adaptive card styling.
"""

import streamlit as st
import sqlite3

from src.analytics.analytics_service import (
    get_total_revenue,
    get_total_orders,
    get_total_customers,
    get_total_products,
    get_average_customer_spending,
)


def render_kpi_cards(connection: sqlite3.Connection, category=None, city=None):
    """
    Render executive KPI metric cards across 5 columns with responsive, theme-adaptive styling.
    Adjusts layout and font scaling to prevent ellipsis truncation or clipping on large values.
    """
    total_rev = get_total_revenue(connection, category=category, city=city)
    total_orders = get_total_orders(connection, category=category, city=city)
    total_customers = get_total_customers(connection, city=city)
    total_products = get_total_products(connection, category=category)
    avg_spend = get_average_customer_spending(connection, category=category, city=city)

    # Scoped responsive styles for the 5 KPI cards
    st.markdown(
        """
        <style>
        /* Scoped KPI cards: compact padding, responsive typography, no truncation */
        div[data-testid="stMetric"] {
            padding: 10px 10px !important;
        }
        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] > div,
        div[data-testid="stMetricValue"] div,
        div[data-testid="stMetricValue"] span {
            overflow: visible !important;
            text-overflow: clip !important;
            white-space: nowrap !important;
        }
        div[data-testid="stMetricValue"] div {
            font-size: clamp(1.0rem, 1.22vw, 1.24rem) !important;
            font-weight: 700 !important;
            line-height: 1.25 !important;
        }
        @media (max-width: 1280px) {
            div[data-testid="stMetric"] {
                padding: 8px 8px !important;
            }
            div[data-testid="stMetricValue"] div {
                font-size: clamp(0.92rem, 1.12vw, 1.14rem) !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Weighted column widths provide extra breathing room for currency/comma values
    c1, c2, c3, c4, c5 = st.columns([1.18, 0.92, 0.90, 0.90, 1.10], gap="small")
    with c1:
        st.metric(label="Total Revenue", value=f"Rs. {total_rev:,.0f}")
    with c2:
        st.metric(label="Total Orders", value=f"{total_orders:,}")
    with c3:
        st.metric(label="Customers", value=f"{total_customers:,}")
    with c4:
        st.metric(label="Active Products", value=f"{total_products:,}")
    with c5:
        st.metric(label="Avg Customer Spend", value=f"Rs. {avg_spend:,.0f}")
