"""
Retrieval confidence utilities for InsightAI RAG.

Determines whether retrieved document chunks are
relevant enough to be used as evidence.
"""


DEFAULT_SIMILARITY_THRESHOLD = 0.45


def validate_retrieval_confidence(
    retrieved_chunks,
    threshold=DEFAULT_SIMILARITY_THRESHOLD,
):
    """
    Check whether the best retrieved chunk
    has sufficient similarity to the question.
    """

    if not retrieved_chunks:
        return False, "No relevant information was retrieved."

    best_score = retrieved_chunks[0]["score"]

    if best_score < threshold:
        return (
            False,
            "The available documents do not contain "
            "sufficiently relevant information to answer "
            "this question confidently.",
        )

    return (
        True,
        "Sufficiently relevant information was retrieved.",
    )