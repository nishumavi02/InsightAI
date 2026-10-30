from src.ai.business_context import format_business_context
from src.llm.llm_service import ask_llm
from src.llm.prompts import EXECUTIVE_SUMMARY_PROMPT


def generate_executive_summary(context):
    """
    Generate AI Executive Summary.
    """

    business_context = format_business_context(context)

    prompt = f"""
{EXECUTIVE_SUMMARY_PROMPT}

{business_context}
"""

    return ask_llm(prompt)