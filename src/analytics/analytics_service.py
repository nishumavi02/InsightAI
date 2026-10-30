"""
Business analytics functions for the InsightAI project.
"""

import sqlite3
from typing import Optional, List, Dict, Any
import pandas as pd


def execute_query(connection: sqlite3.Connection, query: str, params: tuple = ()) -> pd.DataFrame:
    """Execute a SQL query and return a DataFrame."""
    return pd.read_sql_query(query, connection, params=params)


def execute_scalar_query(connection: sqlite3.Connection, query: str, params: tuple = ()):
    """Execute a SQL query that returns a single value."""
    cursor = connection.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    return row[0] if row is not None else 0


def get_total_revenue(
    connection: sqlite3.Connection,
    category: Optional[str] = None,
    city: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> float:
    """Return the total revenue from the orders table with optional filters."""
    query = """
        SELECT ROUND(COALESCE(SUM(o.total_amount), 0), 2)
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE 1=1
    """
    params = []
    if category and category != "All":
        query += " AND p.category = ?"
        params.append(category)
    if city and city != "All":
        query += " AND c.city = ?"
        params.append(city)
    if start_date:
        query += " AND o.order_date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND o.order_date <= ?"
        params.append(end_date)

    return float(execute_scalar_query(connection, query, tuple(params)) or 0.0)


def get_total_orders(
    connection: sqlite3.Connection,
    category: Optional[str] = None,
    city: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> int:
    """Return the total number of orders with optional filters."""
    query = """
        SELECT COUNT(DISTINCT o.order_id)
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        JOIN customers c ON o.customer_id = c.customer_id
        WHERE 1=1
    """
    params = []
    if category and category != "All":
        query += " AND p.category = ?"
        params.append(category)
    if city and city != "All":
        query += " AND c.city = ?"
        params.append(city)
    if start_date:
        query += " AND o.order_date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND o.order_date <= ?"
        params.append(end_date)

    return int(execute_scalar_query(connection, query, tuple(params)) or 0)


def get_total_customers(
    connection: sqlite3.Connection,
    city: Optional[str] = None,
) -> int:
    """Return the total number of customers."""
    query = "SELECT COUNT(*) FROM customers WHERE 1=1"
    params = []
    if city and city != "All":
        query += " AND city = ?"
        params.append(city)
    return int(execute_scalar_query(connection, query, tuple(params)) or 0)


def get_total_products(
    connection: sqlite3.Connection,
    category: Optional[str] = None,
) -> int:
    """Return the total number of products."""
    query = "SELECT COUNT(*) FROM products WHERE 1=1"
    params = []
    if category and category != "All":
        query += " AND category = ?"
        params.append(category)
    return int(execute_scalar_query(connection, query, tuple(params)) or 0)


def get_average_customer_spending(
    connection: sqlite3.Connection,
    category: Optional[str] = None,
    city: Optional[str] = None,
) -> float:
    """Return the average amount spent per customer."""
    query = """
        SELECT ROUND(COALESCE(AVG(customer_total), 0), 2)
        FROM (
            SELECT
                o.customer_id,
                SUM(o.total_amount) AS customer_total
            FROM orders o
            JOIN products p ON o.product_id = p.product_id
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE 1=1
    """
    params = []
    if category and category != "All":
        query += " AND p.category = ?"
        params.append(category)
    if city and city != "All":
        query += " AND c.city = ?"
        params.append(city)
    query += """
            GROUP BY o.customer_id
        )
    """
    return float(execute_scalar_query(connection, query, tuple(params)) or 0.0)


def get_top_products(
    connection: sqlite3.Connection,
    limit: int = 10,
    category: Optional[str] = None,
) -> pd.DataFrame:
    """Return top revenue-generating products as a DataFrame."""
    query = """
        SELECT
            p.product_id,
            p.product_name,
            p.category,
            p.price,
            SUM(o.quantity) AS units_sold,
            ROUND(SUM(o.total_amount), 2) AS total_revenue
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE 1=1
    """
    params = []
    if category and category != "All":
        query += " AND p.category = ?"
        params.append(category)

    query += f"""
        GROUP BY p.product_id, p.product_name, p.category, p.price
        ORDER BY total_revenue DESC
        LIMIT {int(limit)}
    """
    return execute_query(connection, query, tuple(params))


def get_revenue_by_category(connection: sqlite3.Connection) -> pd.DataFrame:
    """Return revenue generated by each product category."""
    query = """
        SELECT
            p.category,
            COUNT(o.order_id) AS total_orders,
            SUM(o.quantity) AS total_units_sold,
            ROUND(SUM(o.total_amount), 2) AS total_revenue
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC
    """
    return execute_query(connection, query)


# Alias for backward compatibility
get_category_revenue = get_revenue_by_category


def get_revenue_by_city(connection: sqlite3.Connection, limit: int = 15) -> pd.DataFrame:
    """Return revenue generated by each city."""
    query = f"""
        SELECT
            c.city,
            c.state,
            COUNT(DISTINCT c.customer_id) AS customer_count,
            COUNT(o.order_id) AS order_count,
            ROUND(SUM(o.total_amount), 2) AS total_revenue
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY c.city, c.state
        ORDER BY total_revenue DESC
        LIMIT {int(limit)}
    """
    return execute_query(connection, query)


def get_top_customers(connection: sqlite3.Connection, limit: int = 10) -> pd.DataFrame:
    """Return the top customers by total spending."""
    query = f"""
        SELECT
            c.customer_id,
            c.customer_name,
            c.city,
            c.state,
            COUNT(o.order_id) AS total_orders,
            ROUND(SUM(o.total_amount), 2) AS total_spent
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY c.customer_id, c.customer_name, c.city, c.state
        ORDER BY total_spent DESC
        LIMIT {int(limit)}
    """
    return execute_query(connection, query)


def get_monthly_revenue_trend(connection: sqlite3.Connection) -> pd.DataFrame:
    """Return monthly aggregated revenue for trend charts."""
    query = """
        SELECT
            strftime('%Y-%m', order_date) AS month,
            COUNT(order_id) AS total_orders,
            ROUND(SUM(total_amount), 2) AS total_revenue
        FROM orders
        GROUP BY month
        ORDER BY month ASC
    """
    return execute_query(connection, query)


def get_distinct_categories(connection: sqlite3.Connection) -> List[str]:
    """Return distinct categories available in products."""
    query = "SELECT DISTINCT category FROM products ORDER BY category"
    df = execute_query(connection, query)
    return ["All"] + df["category"].dropna().tolist()


def get_distinct_cities(connection: sqlite3.Connection) -> List[str]:
    """Return distinct cities available in customers."""
    query = "SELECT DISTINCT city FROM customers ORDER BY city"
    df = execute_query(connection, query)
    return ["All"] + df["city"].dropna().tolist()


def get_date_range(connection: sqlite3.Connection) -> tuple[str, str]:
    """Return minimum and maximum order dates."""
    cursor = connection.cursor()
    cursor.execute("SELECT MIN(order_date), MAX(order_date) FROM orders")
    min_date, max_date = cursor.fetchone()
    return min_date or "2024-01-01", max_date or "2026-12-31"


def get_ai_business_highlights(connection: sqlite3.Connection) -> List[str]:
    """Generate meaningful business highlights from database data."""
    highlights = []
    category_df = get_revenue_by_category(connection)
    city_df = get_revenue_by_city(connection)
    customer_df = get_top_customers(connection)
    total_rev = get_total_revenue(connection)

    if not category_df.empty:
        top_cat = category_df.iloc[0]
        cat_share = (top_cat["total_revenue"] / total_rev * 100) if total_rev else 0
        highlights.append(
            f"🏆 **Dominant Category**: {top_cat['category']} generated ₹{top_cat['total_revenue']:,.2f} ({cat_share:.1f}% of total revenue)."
        )

    if not city_df.empty:
        top_city = city_df.iloc[0]
        highlights.append(
            f"🏙️ **Top Market**: {top_city['city']} ({top_city['state']}) leads all regions with ₹{top_city['total_revenue']:,.2f} in revenue."
        )

    if not customer_df.empty:
        top_cust = customer_df.iloc[0]
        highlights.append(
            f"👑 **VIP Customer**: {top_cust['customer_name']} from {top_cust['city']} contributed ₹{top_cust['total_spent']:,.2f} across {top_cust['total_orders']} orders."
        )

    trend_df = get_monthly_revenue_trend(connection)
    if len(trend_df) >= 2:
        last_month = trend_df.iloc[-1]
        prev_month = trend_df.iloc[-2]
        growth = ((last_month["total_revenue"] - prev_month["total_revenue"]) / prev_month["total_revenue"]) * 100 if prev_month["total_revenue"] else 0
        direction = "grew" if growth >= 0 else "contracted"
        icon = "📈" if growth >= 0 else "📉"
        highlights.append(
            f"{icon} **Recent Trajectory**: Revenue {direction} by {abs(growth):.1f}% from {prev_month['month']} to {last_month['month']}."
        )

    return highlights


def get_key_business_facts(connection: sqlite3.Connection) -> Dict[str, Any]:
    """Return the most important business facts for the dashboard."""
    facts = {}
    facts["total_revenue"] = get_total_revenue(connection)
    facts["total_orders"] = get_total_orders(connection)
    facts["total_customers"] = get_total_customers(connection)
    facts["total_products"] = get_total_products(connection)
    facts["average_spending"] = get_average_customer_spending(connection)

    category_df = get_revenue_by_category(connection)
    facts["top_category"] = category_df.iloc[0].to_dict() if not category_df.empty else {"category": "N/A", "total_revenue": 0}

    city_df = get_revenue_by_city(connection)
    facts["top_city"] = city_df.iloc[0].to_dict() if not city_df.empty else {"city": "N/A", "total_revenue": 0}

    customer_df = get_top_customers(connection)
    facts["top_customer"] = customer_df.iloc[0].to_dict() if not customer_df.empty else {"customer_name": "N/A", "total_spent": 0}

    return facts
