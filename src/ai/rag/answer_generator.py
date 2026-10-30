"""
RAG Answer Generator

Generates business answers strictly grounded in retrieved evidence.
"""

from typing import List, Dict, Any
from src.llm.llm_service import ask_llm


RAG_ANSWER_SYSTEM_PROMPT = """
You are the RAG answer-generation component of InsightAI.

Your job is to answer the user's question using ONLY the provided document evidence.

STRICT EVIDENCE RULES:
1. Use only information explicitly supported by the evidence.
2. Do not use outside knowledge.
3. Do not invent facts, numbers, dates, names, or policies.
4. Do not make assumptions that are not supported by the evidence.
5. You may summarize or rephrase information from the evidence.
6. Every factual claim in your answer must be supported by the provided evidence.
7. If the evidence does not contain enough information to answer the question, clearly state that the available information is insufficient.
8. Never fill missing information using your own knowledge.
9. Do not mention similarity scores or embeddings.
10. Answer in clear, natural business language.
"""


def generate_rag_answer(question: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    """Generate an answer using only approved retrieved evidence."""
    evidence_texts = []
    for item in retrieved_chunks:
        chunk_str = item.get("chunk") or item.get("text", "")
        if chunk_str:
            evidence_texts.append(chunk_str)

    evidence = "\n\n".join(evidence_texts)

    prompt = f"""
User question:
{question}

Retrieved document evidence:
{evidence}

Answer the user's question using only the retrieved evidence.
"""
    return ask_llm(
        prompt=prompt,
        system_prompt=RAG_ANSWER_SYSTEM_PROMPT,
        max_tokens=400,
        temperature=0.1,
    )
