"""Evaluation utilities for generated Q/A pairs."""
from __future__ import annotations

import json
import argparse
from typing import Dict, List

from . import retrieval


def _token_overlap(text: str, reference: str) -> float:
    """Compute ratio of words from text that appear in reference."""
    tokens = text.lower().split()
    if not tokens:
        return 0.0
    ref = reference.lower()
    matches = sum(1 for t in tokens if t in ref)
    return matches / len(tokens)


def self_consistency(question: str, answer: str, context: str) -> float:
    """Check that the answer is supported by the provided context."""
    return _token_overlap(answer, context)


def document_grounding(objective: str, answer: str) -> float:
    """Verify the answer is grounded in retrieved documentation."""
    results = retrieval.query(objective, k=3)
    docs = " ".join(chunk for _, chunk in results)
    return _token_overlap(answer, docs)


def distractor_quality(distractors: List[str], answer: str, context: str) -> float:
    """Check that distractors are relevant but not duplicates of the answer."""
    if not distractors:
        return 0.0
    scores = []
    for d in distractors:
        relevance = _token_overlap(d, context)
        uniqueness = 1 - _token_overlap(d, answer)
        scores.append((relevance + uniqueness) / 2)
    return sum(scores) / len(scores)


def evaluate(qas: List[Dict]) -> float:
    """Return average factual-consistency score for Q/A pairs."""
    scores = []
    for qa in qas:
        obj = qa.get("objective", "")
        answer = qa.get("answer", "")
        question = qa.get("question", "")  # unused but kept for API
        context = qa.get("context", "")
        distractors = qa.get("distractors", [])

        sc = self_consistency(question, answer, context)
        dg = document_grounding(obj, answer)
        dq = distractor_quality(distractors, answer, context)

        scores.append((sc + dg + dq) / 3)
    return sum(scores) / len(scores) if scores else 0.0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate generated exam JSON")
    parser.add_argument("file", help="Path to exam JSON file")
    args = parser.parse_args()

    with open(args.file) as f:
        data = json.load(f)

    score = evaluate(data)
    print(f"Score: {score:.2f}")

