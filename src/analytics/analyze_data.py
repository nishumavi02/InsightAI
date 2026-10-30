"""
Run business analytics queries on the InsightAI database.
"""
from pathlib import Path
import sys

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Make project root importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import DATABASE_FILE

from src.analytics.analytics_service import (
    get_total_revenue,
    get_total_orders,
    get_total_customers,
    get_total_products,
    get_average_customer_spending,
    get_top_products,
    get_category_revenue,
    get_top_customers,
)

def get_connection():
    """Create and return a database connection."""
    connection = sqlite3.connect(DATABASE_FILE)
    return connection

def plot_top_products(top_products):
    """Plot the top revenue-generating products."""

    plt.figure(figsize=(10, 6))

    plt.bar(
        top_products["product_name"],
        top_products["total_revenue"]
    )

    plt.title("Top Revenue-Generating Products")
    plt.xlabel("Product")
    plt.ylabel("Revenue")

    plt.xticks(rotation=45)

    plt.tight_layout()

    from pathlib import Path

    output_dir = Path("reports/charts")
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.savefig(output_dir / "top_products.png", dpi=300)

    plt.show()

def main():
    connection = get_connection()
    print("Database connected successfully.")

    total_revenue = get_total_revenue(connection)
    print(f"Total Revenue: ₹{total_revenue}")
    print(f"Total Orders: {get_total_orders(connection)}")
    print(f"Total Customers: {get_total_customers(connection)}")
    print(f"Total Products: {get_total_products(connection)}")
    print(f"Average Customer Spending: ₹{get_average_customer_spending(connection)}")
    top_products = get_top_products(connection)

    plot_top_products(top_products)
    print("\nTop Revenue-Generating Products:")
    print(top_products)

    category_revenue = get_category_revenue(connection)
    print("\nRevenue by Category:")
    print(category_revenue)

    top_customers = get_top_customers(connection)
    print("\nTop Customers:")
    print(top_customers)

    connection.close()
    print("Database connection closed.")


if __name__ == "__main__":
    main()