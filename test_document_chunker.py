from pathlib import Path

from src.ai.rag.document_loader import load_text_document
from src.ai.rag.document_chunker import chunk_text


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


print("\n--- DOCUMENT CHUNKING SUCCESSFUL ---\n")

print(f"Total chunks: {len(chunks)}")

for index, chunk in enumerate(chunks, start=1):

    print(f"\n--- CHUNK {index} ---")
    print(chunk)