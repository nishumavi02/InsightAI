"""
SQL Result Explainer

Converts exact SQL results into natural-language business answers.
"""

from src.llm.llm_service import ask_llm


SQL_EXPLAINER_SYSTEM_PROMPT = """
You are the explanation layer of an AI business intelligence system.
The database has already executed the calculation.
Your job is ONLY to explain the database result in clear, professional, natural business language.

IMPORTANT RULES:
- Use only the information provided in the SQL result.
- Do not invent facts or guess missing information.
- Do not perform independent calculations or change numbers.
- If the result contains amounts, format with appropriate currency symbols and commas.
- Keep the explanation concise and direct (1-3 sentences).
"""


def explain_sql_result(question: str, sql_result: str) -> str:
    """Convert an exact SQL result into a natural-language answer."""
    prompt = f"""
User question:
{question}

SQL result:
{sql_result}

Provide a concise, professional business explanation based strictly on the SQL result above.
"""
    return ask_llm(
        prompt=prompt,
        system_prompt=SQL_EXPLAINER_SYSTEM_PROMPT,
        max_tokens=250,
        temperature=0.2,
    )
