"""Generate Q/A pairs using a simple LangGraph flow."""
from __future__ import annotations

from typing import Dict, List
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END

from .agents import researcher, questioner, answerer, distractor, reviewer


def should_regenerate(state: QAState) -> str:
    """Decide next step based on quality score and retry count."""

    score = state.get("review_score", 0.0)
    retries = state.get("retries", 0)

    if retries > 2:
        print("Max retries exceeded. Finishing.")
        return END

    if score < 0.5:
        print("Score is very low. Retrying from research.")
        return "research"
    if score < 0.7:
        print("Score is below threshold. Regenerating question.")
        return "question"

    print(f"Score {score:.2f} is acceptable. Finishing.")
    return END


class QAState(TypedDict, total=False):
    """Graph state for a single question/answer."""

    objective: str
    context: str
    sources: List[str]
    question: str
    answer: str
    explanation: str
    distractors: List[str]
    review_score: float
    retries: int


def build_graph():
    sg = StateGraph(QAState)
    sg.add_node("research", researcher)
    sg.add_node("question", questioner)
    sg.add_node("answer", answerer)
    sg.add_node("distractor", distractor)
    sg.add_node("review", reviewer)

    sg.set_entry_point("research")
    sg.add_edge("research", "question")
    sg.add_edge("question", "answer")
    sg.add_edge("answer", "distractor")
    sg.add_edge("distractor", "review")

    sg.add_conditional_edges(
        "review",
        should_regenerate,
        {
            "question": "question",
            "research": "research",
            END: END,
        },
    )
    return sg.compile()


COMP_GRAPH = build_graph()


def generate_exam(objectives: List[str], n: int = 5) -> List[Dict]:
    results = []
    for i in range(min(n, len(objectives))):
        state = {"objective": objectives[i], "retries": 0}
        qa = COMP_GRAPH.invoke(state)
        results.append({
            "objective": objectives[i],
            "question": qa.get("question", ""),
            "answer": qa.get("answer", ""),
            "explanation": qa.get("explanation", ""),
            "distractors": qa.get("distractors", []),
        })
    return results
