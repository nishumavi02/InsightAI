"""
RAG Agent

Coordinates document retrieval, confidence checking,
and evidence-grounded answer generation with source attribution.
"""

from typing import Union, Dict, Any, List, Optional
from pathlib import Path

from src.config import DOCUMENTS_DIR
from src.ai.rag.document_loader import load_documents_from_directory, extract_text_from_file
from src.ai.rag.document_chunker import chunk_text
from src.ai.rag.embedding_service import generate_embeddings
from src.ai.rag.retrieval_service import retrieve_relevant_chunks
from src.ai.rag.retrieval_confidence import validate_retrieval_confidence
from src.ai.rag.answer_generator import generate_rag_answer


_KNOWLEDGE_BASE_CACHE = {
    "chunks": None,
    "embeddings": None,
    "sources": None,
}


def get_default_knowledge_base():
    """Retrieve or initialize the default cached knowledge base."""
    global _KNOWLEDGE_BASE_CACHE
    if _KNOWLEDGE_BASE_CACHE["chunks"] is not None:
        return _KNOWLEDGE_BASE_CACHE["chunks"], _KNOWLEDGE_BASE_CACHE["embeddings"]

    chunks = []
    sources = []

    # Load from documents dir
    docs = load_documents_from_directory(DOCUMENTS_DIR)
    if docs:
        for doc in docs:
            doc_chunks = chunk_text(doc["text"])
            chunks.extend(doc_chunks)
            sources.extend([doc["source"]] * len(doc_chunks))
    else:
        # Fallback to single company_policy.txt if present
        sample_path = DOCUMENTS_DIR / "company_policy.txt"
        if sample_path.exists():
            text = extract_text_from_file(sample_path)
            chunks = chunk_text(text)
            sources = ["company_policy.txt"] * len(chunks)

    if not chunks:
        chunks = ["Company policy: Standard working days are Monday through Friday."]
        sources = ["default_policy.txt"]

    embeddings = generate_embeddings(chunks)
    _KNOWLEDGE_BASE_CACHE["chunks"] = chunks
    _KNOWLEDGE_BASE_CACHE["embeddings"] = embeddings
    _KNOWLEDGE_BASE_CACHE["sources"] = sources

    return chunks, embeddings


def run_rag_agent(
    question: str,
    chunks: Optional[List[str]] = None,
    chunk_embeddings: Optional[Any] = None,
    return_dict: bool = False,
    threshold: float = 0.25,
) -> Union[str, Dict[str, Any]]:
    """
    Run the complete RAG pipeline:
    1. Retrieve relevant document chunks
    2. Check retrieval confidence threshold
    3. Generate grounded answer
    4. Provide source traceability
    """
    if chunks is None or chunk_embeddings is None:
        chunks, chunk_embeddings = get_default_knowledge_base()

    # Step 1: Retrieve relevant chunks
    results = retrieve_relevant_chunks(
        question=question,
        chunks=chunks,
        chunk_embeddings=chunk_embeddings,
        top_k=3,
    )

    # Step 2: Validate retrieval confidence
    is_confident, message = validate_retrieval_confidence(results, threshold=threshold)

    # Step 3: Handle insufficient evidence
    if not is_confident:
        if return_dict:
            return {
                "agent": "RAG",
                "answer": message,
                "confidence": round(float(results[0]["score"]), 3) if results else 0.0,
                "sources": [],
                "evidence": results,
                "is_grounded": False,
            }
        return message

    # Step 4: Generate grounded answer
    answer = generate_rag_answer(question, results)
    best_score = float(results[0]["score"]) if results else 1.0

    if return_dict:
        return {
            "agent": "RAG",
            "answer": answer,
            "confidence": round(min(best_score * 1.5, 0.98), 3),
            "sources": [r.get("source", "company_policy.txt") for r in results],
            "evidence": results,
            "is_grounded": True,
        }

    return answer
