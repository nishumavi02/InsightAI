"""
Embedding service for InsightAI RAG.

Converts text into normalized numerical vectors for semantic similarity search.
Includes in-memory embedding caching to avoid recomputation, and a dual-engine architecture:
Uses SentenceTransformers when available, with a resilient Scikit-learn TF-IDF semantic
vectorizer fallback if OS policies block native PyTorch DLLs.
"""

import hashlib
import numpy as np
from typing import List, Union

_SENTENCE_MODEL = None
_VECTORIZER = None
_CORPUS_VOCAB = set()
_EMBEDDING_CACHE = {}


def _get_sentence_transformer():
    """Lazily load SentenceTransformer model if permitted by the operating system."""
    global _SENTENCE_MODEL
    if _SENTENCE_MODEL is not False and _SENTENCE_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            _SENTENCE_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            # WinError 4551, missing DLL, or torch blocked by Windows App Control
            _SENTENCE_MODEL = False
    return _SENTENCE_MODEL if _SENTENCE_MODEL is not False else None


def _get_tfidf_vectorizer():
    """Fallback TF-IDF vectorizer when neural models cannot be loaded."""
    global _VECTORIZER
    if _VECTORIZER is None:
        from sklearn.feature_extraction.text import TfidfVectorizer
        # Domain vocabulary seed
        seed_corpus = [
            "leave policy paid vacation annual holidays carry forward",
            "remote work manager approval hybrid working days",
            "working week monday friday office hours",
            "notice period resignation employment contract tenure",
            "performance review appraisal evaluation employee promotion",
            "travel reimbursement expense food lodging policy",
            "maternity paternity parental leaves child care",
            "sick medical hospital doctor note leave",
            "revenue product orders customer category sales total profit",
        ]
        _VECTORIZER = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True)
        _VECTORIZER.fit(seed_corpus)
    return _VECTORIZER


def _hash_text(text: str) -> str:
    """Hash string for fast cache lookup."""
    return hashlib.md5(text.strip().encode("utf-8")).hexdigest()


def generate_embedding(text: str) -> np.ndarray:
    """Generate an embedding vector for a single piece of text."""
    if not text or not text.strip():
        raise ValueError("Cannot generate an embedding for empty text.")

    cache_key = _hash_text(text)
    if cache_key in _EMBEDDING_CACHE:
        return _EMBEDDING_CACHE[cache_key]

    model = _get_sentence_transformer()
    if model is not None:
        try:
            embedding = model.encode(text, convert_to_numpy=True)
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
            _EMBEDDING_CACHE[cache_key] = embedding
            return embedding
        except Exception:
            pass

    # Resilient TF-IDF Fallback Vectorizer
    vectorizer = _get_tfidf_vectorizer()
    sparse_vec = vectorizer.transform([text]).toarray()[0]
    norm = np.linalg.norm(sparse_vec)
    embedding = (sparse_vec / norm) if norm > 0 else sparse_vec.astype(np.float32)
    _EMBEDDING_CACHE[cache_key] = embedding
    return embedding


def generate_embeddings(texts: List[str]) -> np.ndarray:
    """Generate embeddings for multiple text chunks."""
    if not texts:
        raise ValueError("Cannot generate embeddings from empty input.")

    embeddings = []
    # If using fallback vectorizer, fit on the incoming corpus + seed for better discrimination
    model = _get_sentence_transformer()
    if model is None:
        global _VECTORIZER
        from sklearn.feature_extraction.text import TfidfVectorizer
        # Update vectorizer on the current text chunks
        _VECTORIZER = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True)
        _VECTORIZER.fit(texts)

    for text in texts:
        embeddings.append(generate_embedding(text))

    return np.array(embeddings, dtype=np.float32)
