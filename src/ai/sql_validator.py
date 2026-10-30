"""
SQL Validator

Validates and sanitizes LLM-generated SQL before execution against SQLite.
Only allows read-only SELECT and WITH statements and rejects destructive commands.
"""

import re
from typing import Tuple


def clean_sql_query(sql: str) -> str:
    """
    Sanitize and extract clean SQL from LLM responses, stripping
    markdown code blocks and extraneous fences.
    """
    if not sql:
        return ""

    cleaned = sql.strip()

    # Strip markdown code blocks: ```sql ... ``` or ``` ... ```
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned)
        cleaned = cleaned.strip()

    # Strip single-line wrapped backticks `SELECT ...`
    if cleaned.startswith("`") and cleaned.endswith("`"):
        cleaned = cleaned.strip("`").strip()

    return cleaned


def validate_sql(sql: str) -> Tuple[bool, str]:
    """
    Validate an LLM-generated SQL query.

    Returns:
        (True, "SQL query is valid and safe.") if the query is safe.
        (False, error_reason) if rejected.
    """
    if not sql or not sql.strip():
        return False, "SQL query is empty."

    sql_clean = clean_sql_query(sql)

    # Reject potentially dangerous SQL operations anywhere in the query
    forbidden_keywords = [
        "DROP ",
        "DELETE ",
        "UPDATE ",
        "INSERT ",
        "ALTER ",
        "CREATE ",
        "ATTACH ",
        "DETACH ",
        "REPLACE ",
        "PRAGMA ",
        "TRUNCATE ",
        "EXEC ",
        "GRANT ",
        "REVOKE ",
    ]

    sql_upper = sql_clean.upper()

    for keyword in forbidden_keywords:
        if keyword in sql_upper:
            return False, f"Forbidden SQL operation detected: {keyword.strip()}"

    # Only allow read-only queries starting with SELECT or WITH
    if not (sql_upper.startswith("SELECT") or sql_upper.startswith("WITH")):
        return False, "Only SELECT and WITH queries are allowed."

    # Disallow multiple semicolon statements (prevent injection chaining)
    statements = [stmt.strip() for stmt in sql_clean.split(";") if stmt.strip()]
    if len(statements) > 1:
        return False, "Multiple SQL statements in a single query are forbidden."

    return True, "SQL query is valid and safe."
