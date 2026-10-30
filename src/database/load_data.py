"""
Load generated CSV datasets into SQLite database.
"""

import csv
import sqlite3
from pathlib import Path

from src.config import (
    DATABASE_FILE,
    CUSTOMERS_FILE,
    PRODUCTS_FILE,
    ORDERS_FILE,
    SCHEMA_FILE,
)


def init_db(connection):
    """Ensure database schema is created."""
    if SCHEMA_FILE.exists():
        schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")
        cursor = connection.cursor()
        cursor.executescript(schema_sql)
        connection.commit()


def load_csv(file_path):
    """Read a CSV file and return all data rows."""
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return list(reader)


def insert_data(connection, delete_query, insert_query, rows):
    """Insert rows into a database table."""
    cursor = connection.cursor()
    cursor.execute(delete_query)
    cursor.executemany(insert_query, rows)
    connection.commit()


def main():
    print("Loading datasets into SQLite...")
    connection = sqlite3.connect(DATABASE_FILE)
    print("Database connected successfully.")

    # Initialize schema first
    init_db(connection)

    # Load CSV files
    customer_rows = load_csv(CUSTOMERS_FILE)
    product_rows = load_csv(PRODUCTS_FILE)
    order_rows = load_csv(ORDERS_FILE)

    # Insert customers
    insert_data(
        connection,
        "DELETE FROM customers",
        """
        INSERT INTO customers (
            customer_id,
            customer_name,
            age,
            gender,
            city,
            state
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        customer_rows,
    )

    # Insert products
    insert_data(
        connection,
        "DELETE FROM products",
        """
        INSERT INTO products (
            product_id,
            product_name,
            category,
            price,
            inventory_level
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        product_rows,
    )

    # Insert orders
    insert_data(
        connection,
        "DELETE FROM orders",
        """
        INSERT INTO orders (
            order_id,
            customer_id,
            product_id,
            order_date,
            quantity,
            total_amount
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        order_rows,
    )

    # Verify import
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM customers")
    customer_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]

    print(f"Customers in database: {customer_count}")
    print(f"Products in database: {product_count}")
    print(f"Orders in database: {order_count}")

    connection.close()
    print("Database connection closed.")


if __name__ == "__main__":
    main()
