"""
Semantic retrieval service for InsightAI RAG.

Finds document chunks that are most relevant
to a user's question.
"""

import numpy as np

from src.ai.rag.embedding_service import (
    generate_embedding,
)


def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two vectors.
    """

    denominator = (
        np.linalg.norm(vector_a)
        * np.linalg.norm(vector_b)
    )

    if denominator == 0:
        return 0.0

    return float(
        np.dot(vector_a, vector_b)
        / denominator
    )


def retrieve_relevant_chunks(
    question,
    chunks,
    chunk_embeddings,
    top_k=3,
):
    """
    Retrieve the most relevant document chunks
    for a user question.
    """

    if not question or not question.strip():
        raise ValueError(
            "Question cannot be empty."
        )

    if not chunks:
        raise ValueError(
            "No document chunks available."
        )

    if len(chunks) != len(chunk_embeddings):
        raise ValueError(
            "Number of chunks and embeddings must match."
        )

    question_embedding = generate_embedding(
        question
    )

    scored_chunks = []

    for index, chunk in enumerate(chunks):

        score = cosine_similarity(
            question_embedding,
            chunk_embeddings[index]
        )

        scored_chunks.append(
            {
                "chunk": chunk,
                "score": score,
            }
        )

    scored_chunks.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return scored_chunks[:top_k]