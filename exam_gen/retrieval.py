from math import sqrt
from typing import List, Tuple

from .embeddings import embed_texts
from . import db


def _cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sqrt(sum(x * x for x in a))
    nb = sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _mmr(query_emb: List[float], cand_embs: List[List[float]], k: int, lambd: float = 0.5) -> List[int]:
    """Return indices selected via Maximal Marginal Relevance."""
    selected: List[int] = []
    candidates = list(range(len(cand_embs)))
    while candidates and len(selected) < k:
        best_idx = candidates[0]
        best_score = -1e9
        for idx in candidates:
            sim_to_query = _cosine(query_emb, cand_embs[idx])
            sim_to_selected = max(
                (_cosine(cand_embs[idx], cand_embs[j]) for j in selected), default=0
            )
            score = lambd * sim_to_query - (1 - lambd) * sim_to_selected
            if score > best_score:
                best_score = score
                best_idx = idx
        selected.append(best_idx)
        candidates.remove(best_idx)
    return selected


def query(text: str, k: int = 5) -> List[Tuple[str, str]]:
    """Return ``k`` diverse chunks most relevant to ``text`` using MMR."""

    emb = embed_texts([text])[0]
    raw = db.search(emb, top_k=k * 4)
    if not raw:
        return []

    chunks = [c for _, c in raw]
    cand_embs = embed_texts(chunks)
    idxs = _mmr(emb, cand_embs, k)
    return [raw[i] for i in idxs]

