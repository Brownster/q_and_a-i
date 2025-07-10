"""Agent implementations for question generation."""
from typing import Dict

from . import retrieval
from .llm import chat


def researcher(state: Dict) -> Dict:
    """Retrieve supporting context for the objective."""
    objective = state.get("objective", "")
    chunks = retrieval.query(objective, k=2)
    context = " ".join(chunk for _, chunk in chunks)
    return {"context": context}


def questioner(state: Dict) -> Dict:
    context = state.get("context", "")
    prompt = [
        {"role": "system", "content": "Write one Terraform exam question."},
        {"role": "user", "content": context},
    ]
    question = chat(prompt)
    return {"question": question}


def answerer(state: Dict) -> Dict:
    context = state.get("context", "")
    question = state.get("question", "")
    prompt = [
        {"role": "system", "content": "Answer the question and explain."},
        {"role": "user", "content": f"Context: {context}\nQuestion: {question}"},
    ]
    text = chat(prompt)
    if "Explanation:" in text:
        ans, exp = text.split("Explanation:", 1)
        return {"answer": ans.strip(), "explanation": exp.strip()}
    return {"answer": text.strip(), "explanation": ""}


def reviewer(state: Dict) -> Dict:
    # Placeholder reviewer; accept result
    return {}
