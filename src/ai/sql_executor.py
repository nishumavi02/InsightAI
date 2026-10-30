"""
SQL Executor

Executes validated read-only SQL queries
against the InsightAI SQLite database.
"""

import pandas as pd


def execute_sql(connection, sql: str) -> pd.DataFrame:
    """
    Execute a validated SQL query and return the result as a DataFrame.

    Args:
        connection: Active SQLite database connection.
        sql: Validated SQL query.

    Returns:
        pandas DataFrame containing the SQL result.

    Raises:
        ValueError: If the SQL query is empty.
        RuntimeError: If the SQL query fails during execution.
    """

    if not sql or not sql.strip():
        raise ValueError("SQL query is empty.")

    try:
        result = pd.read_sql_query(sql, connection)

        return result

    except Exception as error:
        raise RuntimeError(
            f"SQL execution failed: {error}"
        ) from error