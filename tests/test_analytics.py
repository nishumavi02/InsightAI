"""
Unit tests for InsightAI Business Analytics Service.
"""

import pytest
import pandas as pd

from src.analytics.analytics_service import (
    get_total_revenue,
    get_total_orders,
    get_total_customers,
    get_total_products,
    get_average_customer_spending,
    get_top_products,
    get_revenue_by_category,
    get_revenue_by_city,
    get_top_customers,
    get_monthly_revenue_trend,
    get_key_business_facts,
    get_ai_business_highlights,
)


def test_core_kpis(db_connection):
    rev = get_total_revenue(db_connection)
    orders = get_total_orders(db_connection)
    custs = get_total_customers(db_connection)
    prods = get_total_products(db_connection)
    avg_spend = get_average_customer_spending(db_connection)

    assert rev > 0, "Revenue should be positive"
    assert orders == 5000, f"Expected 5000 orders, got {orders}"
    assert custs == 500, f"Expected 500 customers, got {custs}"
    assert prods == 50, f"Expected 50 products, got {prods}"
    assert avg_spend > 0, "Average spending should be positive"


def test_analytics_filters(db_connection):
    electronics_rev = get_total_revenue(db_connection, category="Electronics")
    all_rev = get_total_revenue(db_connection)

    assert electronics_rev > 0
    assert electronics_rev < all_rev, "Filtered category revenue should be less than total revenue"


def test_dataframes_structure(db_connection):
    top_p = get_top_products(db_connection, limit=5)
    assert len(top_p) == 5
    assert "total_revenue" in top_p.columns
    assert "product_name" in top_p.columns

    cat_df = get_revenue_by_category(db_connection)
    assert not cat_df.empty
    assert "category" in cat_df.columns
    assert "total_revenue" in cat_df.columns

    city_df = get_revenue_by_city(db_connection, limit=5)
    assert len(city_df) <= 5
    assert "city" in city_df.columns

    top_c = get_top_customers(db_connection, limit=5)
    assert len(top_c) == 5
    assert "total_spent" in top_c.columns


def test_business_facts_and_highlights(db_connection):
    facts = get_key_business_facts(db_connection)
    assert "total_revenue" in facts
    assert "top_category" in facts
    assert "top_city" in facts
    assert "top_customer" in facts

    highlights = get_ai_business_highlights(db_connection)
    assert isinstance(highlights, list)
    assert len(highlights) >= 2
