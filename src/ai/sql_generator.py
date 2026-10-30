"""
SQL Generator

Converts natural-language business questions into valid SQLite SQL queries
based on the provided database schema.
"""

from src.llm.llm_service import ask_llm


SQL_GENERATOR_SYSTEM_PROMPT = """
You are the SQL generation component of InsightAI.

Your job is to convert a user's natural-language business question into a valid SQLite SQL query.

Important rules:
1. Use ONLY tables and columns provided in the database schema.
2. Do not invent tables or columns.
3. Generate SQLite-compatible SQL.
4. Do not calculate or guess the answer yourself.
5. The SQL query must perform the required calculations.
6. The SQL query must return all important information needed to answer the user's question.
7. When the question asks for a top, highest, lowest, maximum, minimum, or ranking result, return the identifying entity and the relevant calculated metric.
8. Include useful contextual columns when they are directly available and relevant.
9. For revenue questions, return the calculated revenue value.
10. Use appropriate JOIN, GROUP BY, ORDER BY, aggregate functions, filters, and LIMIT clauses when required.
11. Do not include unnecessary columns.
12. Return ONLY the SQL query.
13. Do not use markdown code fences.
14. Do not add explanations.
"""


def generate_sql(question: str, schema: str) -> str:
    """Convert a natural-language question into an SQLite query."""
    prompt = f"""
Database schema:
{schema}

User question:
{question}

Generate the SQLite SQL query required to answer the question.
Return ONLY the SQL query.
"""
    sql = ask_llm(
        prompt=prompt,
        system_prompt=SQL_GENERATOR_SYSTEM_PROMPT,
        max_tokens=300,
        temperature=0.0,
    )
    return sql.strip()
