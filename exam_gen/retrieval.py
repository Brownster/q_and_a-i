from .embeddings import embed_texts
from . import db


def query(text: str, k: int = 5):
    emb = embed_texts([text])[0]
    return db.search(emb, top_k=k)

