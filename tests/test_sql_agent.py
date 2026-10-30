"""
Unit tests for InsightAI SQL Agent.
"""

import pytest
import pandas as pd

from src.ai.sql_validator import validate_sql, clean_sql_query
from src.ai.sql_executor import execute_sql
from src.ai.sql_agent import run_sql_agent


def test_sql_validator_safe_queries():
    is_valid, msg = validate_sql("SELECT * FROM customers;")
    assert is_valid is True

    is_valid, msg = validate_sql("WITH top_c AS (SELECT * FROM customers) SELECT * FROM top_c;")
    assert is_valid is True

    # Code fences stripping
    fenced = "```sql\nSELECT customer_id FROM customers;\n```"
    cleaned = clean_sql_query(fenced)
    assert not cleaned.startswith("```")
    is_valid, msg = validate_sql(fenced)
    assert is_valid is True


def test_sql_validator_rejects_dangerous_queries():
    dangerous = [
        "DROP TABLE customers;",
        "DELETE FROM orders WHERE order_id = '1';",
        "UPDATE products SET price = 0;",
        "INSERT INTO customers VALUES ('c1', 'test', 20, 'M', 'Noida', 'UP');",
        "SELECT * FROM customers; DROP TABLE orders;",
    ]
    for q in dangerous:
        is_valid, msg = validate_sql(q)
        assert is_valid is False, f"Expected query to be rejected: {q}"


def test_sql_executor_success(db_connection):
    df = execute_sql(db_connection, "SELECT COUNT(*) AS total FROM customers;")
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["total"] == 500


def test_run_sql_agent_structured(db_connection):
    res = run_sql_agent("What is the total revenue?", db_connection, return_dict=True)
    assert isinstance(res, dict)
    assert res["agent"] == "SQL"
    assert "answer" in res
    assert res["confidence"] > 0.5
