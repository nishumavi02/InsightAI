"""
ML data preparation utilities for InsightAI.

Responsible for preparing historical business data
for machine-learning and forecasting tasks.
"""

import pandas as pd


def get_monthly_revenue(connection):
    """
    Retrieve monthly revenue from the SQLite database.
    """

    query = """
        SELECT
            strftime('%Y-%m', order_date) AS month,
            SUM(total_amount) AS total_revenue
        FROM orders
        GROUP BY month
        ORDER BY month
    """

    dataframe = pd.read_sql_query(
        query,
        connection
    )

    if dataframe.empty:
        raise ValueError(
            "No historical revenue data found."
        )

    dataframe["month"] = pd.to_datetime(
        dataframe["month"]
    )

    dataframe["total_revenue"] = pd.to_numeric(
        dataframe["total_revenue"]
    )

    return dataframe