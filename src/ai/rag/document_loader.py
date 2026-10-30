"""
Document loader for the InsightAI RAG system.

Loads business documents (.txt, .md, .pdf) from disk or directories,
extracting clean text with source metadata.
"""

from pathlib import Path
from typing import List, Dict, Any, Union


def extract_text_from_file(file_path: Union[str, Path]) -> str:
    """Extract raw text from a single file based on extension."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    suffix = path.suffix.lower()
    if suffix in [".txt", ".md"]:
        text = path.read_text(encoding="utf-8", errors="ignore")
    elif suffix == ".pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(str(path))
            pages = [page.extract_text() or "" for page in reader.pages]
            text = "\n\n".join(pages)
        except Exception as exc:
            raise ValueError(f"Failed to read PDF document '{path.name}': {exc}") from exc
    else:
        raise ValueError(f"Unsupported file format '{suffix}'. Supported: .txt, .md, .pdf")

    text = text.strip()
    if not text:
        raise ValueError(f"The document '{path.name}' is empty.")
    return text


def load_text_document(file_path: Union[str, Path]) -> str:
    """
    Load a text document and return its contents.
    Preserves exact backward compatibility with legacy loader.
    """
    return extract_text_from_file(file_path)


def load_documents_from_directory(directory_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """
    Load all supported business documents from a directory.
    Returns a list of dicts: [{"source": filename, "text": content, "path": Path}].
    """
    dir_path = Path(directory_path)
    if not dir_path.exists() or not dir_path.is_dir():
        return []

    documents = []
    supported_extensions = [".txt", ".md", ".pdf"]
    for file_path in dir_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            try:
                content = extract_text_from_file(file_path)
                documents.append({
                    "source": file_path.name,
                    "text": content,
                    "path": str(file_path),
                })
            except Exception:
                continue

    return documents
