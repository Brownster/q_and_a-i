"""Agent implementations for building a question and answer pair."""

from typing import Dict

from . import retrieval
from .llm import chat, chat_structured, chat_list
from .quality import evaluate


def researcher(state: Dict) -> Dict:
    """Retrieve supporting context and sources for the objective."""
    objective = state.get("objective", "")
    results = retrieval.query(objective, k=2)
    context = " ".join(chunk for _, chunk in results)
    sources = list({src for src, _ in results})
    return {"context": context, "sources": sources}


def questioner(state: Dict) -> Dict:
    """Generate a single exam question."""
    context = state.get("context", "")
    # track how many times we've attempted to generate
    retries = state.get("retries", 0) + 1
    state["retries"] = retries
    prompt = [
        {"role": "system", "content": "Write one Terraform exam question."},
        {"role": "user", "content": context},
    ]
    question = chat(prompt)
    return {"question": question, "retries": retries}


def answerer(state: Dict) -> Dict:
    """Answer the question and cite documentation links."""
    context = state.get("context", "")
    question = state.get("question", "")
    sources = state.get("sources", [])

    source_text = "\n".join(f"- {s}" for s in sources)

    prompt = [
        {
            "role": "system",
            "content": (
                "You are an expert Terraform certification exam writer. "
                "Answer the user's question and provide a detailed explanation. "
                "In the explanation, cite the provided sources as markdown links."
            ),
        },
        {
            "role": "user",
            "content": f"Context: {context}\n\nSources:\n{source_text}\n\nQuestion: {question}",
        },
    ]

    resp = chat_structured(prompt)
    return {
        "answer": resp.get("answer", ""),
        "explanation": resp.get("explanation", ""),
    }


def distractor(state: Dict) -> Dict:
    """Generate plausible but incorrect answers."""
    context = state.get("context", "")
    question = state.get("question", "")
    answer = state.get("answer", "")

    prompt = [
        {
            "role": "system",
            "content": (
                "Given the context, question, and correct answer, generate three "
                "plausible but incorrect answers for a multiple-choice exam."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Context: {context}\nQuestion: {question}\nCorrect Answer: {answer}\n"
                "Provide three wrong answers as a JSON list."
            ),
        },
    ]

    resp = chat_list(prompt)
    return {"distractors": resp.get("distractors", [])}


def reviewer(state: Dict) -> Dict:
    """Evaluate the generated pair using built-in heuristics."""
    score = evaluate([state])
    return {"review_score": score}
