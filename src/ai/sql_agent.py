"""
SQL Agent

Coordinates schema inspection, SQL generation, validation, safe execution,
error recovery, and natural-language result explanation.
"""

import sqlite3
import pandas as pd
from typing import Union, Dict, Any

from src.ai.sql_schema import get_database_schema
from src.ai.sql_generator import generate_sql
from src.ai.sql_validator import validate_sql, clean_sql_query
from src.ai.sql_executor import execute_sql
from src.ai.sql_explainer import explain_sql_result


def regenerate_sql(question: str, schema: str, previous_sql: str, error_message: str) -> str:
    """Ask the LLM to correct a failed SQL query."""
    recovery_prompt = f"""
The SQL query generated for the user's question failed during execution.

Database schema:
{schema}

User question:
{question}

Previous SQL query:
{previous_sql}

Database error:
{error_message}

Generate a corrected SQLite SQL query.
Important rules:
1. Use only tables and columns from the provided schema.
2. Correct the problem causing the database error.
3. Do not change the meaning of the user's question.
4. Do not calculate the answer yourself.
5. Return ONLY the corrected SQL query without markdown code fences or explanations.
"""
    corrected = generate_sql(recovery_prompt, schema)
    return clean_sql_query(corrected)


def run_sql_agent(
    question: str,
    connection: sqlite3.Connection,
    return_dict: bool = False,
) -> Union[str, Dict[str, Any]]:
    """
    Run the complete SQL Agent pipeline:
    1. Inspect DB schema
    2. Generate SQL from question
    3. Clean and validate SQL
    4. Execute SQL with automatic 1-step recovery
    5. Explain result
    """
    schema = get_database_schema(connection)

    # Step 1: Generate SQL
    raw_sql = generate_sql(question, schema)
    sql_query = clean_sql_query(raw_sql)

    # Step 2: Validate SQL
    is_valid, validation_msg = validate_sql(sql_query)
    if not is_valid:
        error_msg = f"SQL validation failed: {validation_msg}"
        if return_dict:
            return {
                "agent": "SQL",
                "answer": error_msg,
                "sql_query": sql_query,
                "data": None,
                "confidence": 0.0,
                "error": validation_msg,
            }
        return error_msg

    # Step 3: Execute SQL with recovery fallback
    result = None
    try:
        result = execute_sql(connection, sql_query)
    except Exception as exec_error:
        # One recovery attempt
        try:
            recovered_sql = regenerate_sql(question, schema, sql_query, str(exec_error))
            is_valid_rec, rec_msg = validate_sql(recovered_sql)
            if not is_valid_rec:
                fail_msg = f"Recovered SQL validation failed: {rec_msg}"
                if return_dict:
                    return {
                        "agent": "SQL",
                        "answer": fail_msg,
                        "sql_query": recovered_sql,
                        "data": None,
                        "confidence": 0.0,
                        "error": rec_msg,
                    }
                return fail_msg
            result = execute_sql(connection, recovered_sql)
            sql_query = recovered_sql
        except Exception as retry_err:
            fail_msg = f"SQL execution failed after recovery attempt: {retry_err}"
            if return_dict:
                return {
                    "agent": "SQL",
                    "answer": fail_msg,
                    "sql_query": sql_query,
                    "data": None,
                    "confidence": 0.0,
                    "error": str(retry_err),
                }
            return fail_msg

    # Step 4: Check if query returned empty data
    if result is None or result.empty:
        empty_msg = "I could not find any matching records in the database for this question."
        if return_dict:
            return {
                "agent": "SQL",
                "answer": empty_msg,
                "sql_query": sql_query,
                "data": pd.DataFrame(),
                "confidence": 0.6,
            }
        return empty_msg

    # Step 5: Explain result in natural business language
    sql_result_str = result.to_string(index=False)
    answer = explain_sql_result(question, sql_result_str)

    if return_dict:
        return {
            "agent": "SQL",
            "answer": answer,
            "sql_query": sql_query,
            "data": result,
            "confidence": 0.95,
        }

    return answer
