from pathlib import Path

from src.ai.rag.document_loader import load_text_document
from src.ai.rag.document_chunker import chunk_text
from src.ai.rag.embedding_service import generate_embeddings
from src.ai.rag.rag_agent import run_rag_agent


PROJECT_ROOT = Path.cwd()

DOCUMENT_PATH = (
    PROJECT_ROOT
    / "data"
    / "documents"
    / "company_policy.txt"
)


# 1. Load document
text = load_text_document(
    DOCUMENT_PATH
)


# 2. Create document chunks
chunks = chunk_text(
    text
)


# 3. Generate embeddings
chunk_embeddings = generate_embeddings(
    chunks
)


# 4. Ask a RAG question
question = (
    "How many unused paid leave days "
    "can an employee carry forward?"
)


# 5. Run complete RAG Agent
answer = run_rag_agent(
    question,
    chunks,
    chunk_embeddings,
)


print("\n--- RAG AGENT ANSWER ---")
print(answer)