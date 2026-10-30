from pathlib import Path

from src.ai.rag.document_loader import load_text_document
from src.ai.rag.document_chunker import chunk_text
from src.ai.rag.embedding_service import generate_embeddings


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

embeddings = generate_embeddings(
    chunks
)


print("\n--- EMBEDDING GENERATION SUCCESSFUL ---\n")

print(f"Total chunks: {len(chunks)}")

print(
    f"Embedding shape: {embeddings.shape}"
)

for index, chunk in enumerate(
    chunks,
    start=1
):

    print(
        f"\nChunk {index}: "
        f"{chunk}"
    )

    print(
        f"Vector dimensions: "
        f"{len(embeddings[index - 1])}"
    )