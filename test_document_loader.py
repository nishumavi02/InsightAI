from pathlib import Path

from src.ai.rag.document_loader import load_text_document


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

print("\n--- DOCUMENT LOADED SUCCESSFULLY ---\n")

print(text)