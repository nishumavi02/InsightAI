"""
Unit tests for InsightAI RAG Agent.
"""

import pytest
import numpy as np

from src.ai.rag.document_loader import extract_text_from_file, load_documents_from_directory
from src.ai.rag.document_chunker import chunk_text
from src.ai.rag.embedding_service import generate_embedding, generate_embeddings
from src.ai.rag.retrieval_service import retrieve_relevant_chunks, cosine_similarity
from src.ai.rag.retrieval_confidence import validate_retrieval_confidence
from src.ai.rag.rag_agent import run_rag_agent


def test_document_loader_and_chunker(sample_documents_dir):
    doc_path = sample_documents_dir / "company_policy.txt"
    assert doc_path.exists()

    text = extract_text_from_file(doc_path)
    assert len(text) > 0
    assert "paid leave" in text.lower()

    chunks = chunk_text(text)
    assert len(chunks) >= 5


def test_embedding_and_retrieval(sample_documents_dir):
    doc_path = sample_documents_dir / "company_policy.txt"
    text = extract_text_from_file(doc_path)
    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)

    assert len(embeddings) == len(chunks)
    assert embeddings.ndim == 2

    # Query semantic retrieval
    results = retrieve_relevant_chunks("Can employees work from home?", chunks, embeddings, top_k=2)
    assert len(results) == 2
    assert "remotely" in results[0]["chunk"].lower() or "approval" in results[0]["chunk"].lower()


def test_retrieval_confidence_rejection():
    # Irrelevant query check
    dummy_results = [{"chunk": "Company leave rules", "score": 0.05}]
    is_conf, msg = validate_retrieval_confidence(dummy_results, threshold=0.35)
    assert is_conf is False


def test_run_rag_agent_grounded():
    res = run_rag_agent("Can employees work remotely with manager approval?", return_dict=True)
    assert isinstance(res, dict)
    assert res["agent"] == "RAG"
    assert res["is_grounded"] is True
    assert "answer" in res
