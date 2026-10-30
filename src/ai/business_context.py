"""
Business Context Builder

Collects all business information required by AI.
"""

from src.analytics.analytics_service import (
    get_total_revenue,
    get_total_orders,
    get_total_customers,
    get_total_products,
    get_revenue_by_category,
    get_top_products,
    get_revenue_by_city,
    get_key_business_facts,
)

def build_business_context(connection):
    """
    Build business context for AI.
    """

    context = {
    "total_revenue": get_total_revenue(connection),
    "total_orders": get_total_orders(connection),
    "total_customers": get_total_customers(connection),
    "total_products": get_total_products(connection),
    }

    return context

def format_business_context(context):
    """
    Convert business context into an LLM-friendly format.
    """

    return f"""
Business Overview

Total Revenue: {context["total_revenue"]}

Total Orders: {context["total_orders"]}

Total Customers: {context["total_customers"]}

Total Products: {context["total_products"]}
"""