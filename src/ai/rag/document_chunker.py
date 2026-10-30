"""
Document chunking utilities for InsightAI RAG.

Splits loaded business documents into meaningful, overlapping chunks
suitable for embedding and semantic search.
"""

from typing import List, Dict, Any, Union


def chunk_text(text: str) -> List[str]:
    """
    Split document text into paragraph-based chunks.
    Preserves exact backward compatibility.
    """
    if not text or not text.strip():
        raise ValueError("Cannot create chunks from empty text.")

    paragraphs = text.split("\n\n")
    chunks = []
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph:
            chunks.append(paragraph)

    return chunks


def chunk_documents_with_metadata(
    documents: List[Dict[str, Any]],
    chunk_size: int = 300,
) -> List[Dict[str, Any]]:
    """
    Chunk multiple loaded documents with source traceability.
    Returns: [{"text": chunk_str, "source": doc_name, "chunk_id": int}]
    """
    chunk_records = []
    global_id = 0

    for doc in documents:
        source_name = doc.get("source", "Unknown Document")
        text = doc.get("text", "")
        raw_chunks = chunk_text(text)

        for raw_chunk in raw_chunks:
            # If paragraph is very large, split into sentences/smaller pieces
            if len(raw_chunk) > chunk_size * 2:
                sentences = raw_chunk.split(". ")
                sub_chunk = ""
                for s in sentences:
                    if len(sub_chunk) + len(s) < chunk_size:
                        sub_chunk += (s + ". ")
                    else:
                        if sub_chunk.strip():
                            chunk_records.append({
                                "text": sub_chunk.strip(),
                                "source": source_name,
                                "chunk_id": global_id,
                            })
                            global_id += 1
                        sub_chunk = s + ". "
                if sub_chunk.strip():
                    chunk_records.append({
                        "text": sub_chunk.strip(),
                        "source": source_name,
                        "chunk_id": global_id,
                    })
                    global_id += 1
            else:
                chunk_records.append({
                    "text": raw_chunk.strip(),
                    "source": source_name,
                    "chunk_id": global_id,
                })
                global_id += 1

    return chunk_records
