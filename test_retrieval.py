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


PROJECT_ROOT = Path.cwd()

DOCUMENT_PATH = (
    PROJECT_ROOT
    / "data"
    / "documents"
    / "company_policy.txt"
)


# Step 1: Load document
text = load_text_document(
    DOCUMENT_PATH
)


# Step 2: Create chunks
chunks = chunk_text(text)


# Step 3: Generate embeddings
chunk_embeddings = generate_embeddings(
    chunks
)


# Step 4: Ask a semantic question
question = (
    "Can employees work from home?"
)


# Step 5: Retrieve relevant chunks
results = retrieve_relevant_chunks(
    question,
    chunks,
    chunk_embeddings,
    top_k=3,
)


print("\n--- SEMANTIC RETRIEVAL ---\n")

print(
    f"Question: {question}"
)

for index, result in enumerate(
    results,
    start=1
):

    print(
        f"\n--- RESULT {index} ---"
    )

    print(
        f"Similarity Score: "
        f"{result['score']:.4f}"
    )

    print(
        f"Chunk: "
        f"{result['chunk']}"
    )
