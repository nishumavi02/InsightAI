import sqlite3
from pathlib import Path

from src.config import DATABASE_FILE

from src.ai.agent_orchestrator import run_agent
from src.ai.rag.document_loader import load_text_document
from src.ai.rag.document_chunker import chunk_text
from src.ai.rag.embedding_service import generate_embeddings


# -----------------------------
# Database
# -----------------------------

connection = sqlite3.connect(
    DATABASE_FILE
)


# -----------------------------
# RAG knowledge base
# -----------------------------

PROJECT_ROOT = Path.cwd()

DOCUMENT_PATH = (
    PROJECT_ROOT
    / "data"
    / "documents"
    / "company_policy.txt"
)

text = load_text_document(
    DOCUMENT_PATH
)

chunks = chunk_text(text)

chunk_embeddings = generate_embeddings(
    chunks
)


# -----------------------------
# Questions
# -----------------------------

questions = [

    "Which customer generated the highest revenue?",

    "How many paid leave days does an employee receive?",

]


# -----------------------------
# Run Agent Orchestrator
# -----------------------------

for question in questions:

    print("\n====================================")

    print(
        f"Question: {question}"
    )

    answer = run_agent(
        question,
        connection,
        chunks,
        chunk_embeddings
    )

    print(
        f"\nInsightAI Answer:\n{answer}"
    )


connection.close()