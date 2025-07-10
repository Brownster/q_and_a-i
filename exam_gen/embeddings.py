import hashlib
import os
from typing import List

import openai

MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

openai.api_key = os.getenv("OPENAI_API_KEY")


def embed_texts(texts: List[str]) -> List[List[float]]:
    if not openai.api_key:
        # Fallback deterministic embedding for tests
        return [_hash_embedding(t) for t in texts]
    response = openai.embeddings.create(model=MODEL, input=texts)
    return [d.embedding for d in response.data]


def _hash_embedding(text: str) -> List[float]:
    h = hashlib.sha256(text.encode()).digest()
    # return 1536-dim deterministic pseudo-embedding
    return [b / 255 for b in h] * (1536 // len(h))

