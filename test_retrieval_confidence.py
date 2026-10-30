from pathlib import Path

from src.ai.rag.document_loader import (
    load_text_document,
)

from src.ai.rag.document_chunker import (
    chunk_text,
)

from src.ai.rag.embedding_service import (
    generate_embeddings,
)

from src.ai.rag.retrieval_service import (
    retrieve_relevant_chunks,
)

from src.ai.rag.retrieval_confidence import (
    validate_retrieval_confidence,
)


PROJECT_ROOT = Path.cwd()

DOCUMENT_PATH = (
    PROJECT_ROOT
    / "data"
    / "documents"
    / "company_policy.txt"
)


# Load document
text = load_text_document(
    DOCUMENT_PATH
)


# Create chunks
chunks = chunk_text(text)


# Generate chunk embeddings
chunk_embeddings = generate_embeddings(
    chunks
)


questions = [
    "How many vacation days does an employee receive?",
    "Can employees work from home?",
    "What is the company's stock market price?",
]


for question in questions:

    print("\n====================================")
    print(f"Question: {question}")
    print("====================================")

    results = retrieve_relevant_chunks(
        question,
        chunks,
        chunk_embeddings,
        top_k=3,
    )

    is_confident, message = (
        validate_retrieval_confidence(
            results
        )
    )

    print(
        f"\nBest similarity score: "
        f"{results[0]['score']:.4f}"
    )

    print(
        f"Confidence check: "
        f"{is_confident}"
    )

    print(
        f"Message: {message}"
    )

    if is_confident:

        print("\nRetrieved evidence:")

        for result in results:

            print(
                f"- "
                f"({result['score']:.4f}) "
                f"{result['chunk']}"
            )

    else:

        print(
            "\nInsightAI will NOT answer "
            "from this evidence."
        )