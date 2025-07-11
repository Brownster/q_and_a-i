"""Generate Q/A pairs using a simple LangGraph flow."""
from typing import Dict, List
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END

from .agents import researcher, questioner, answerer, reviewer


class QAState(TypedDict, total=False):
    """Graph state for a single question/answer."""

    objective: str
    context: str
    sources: List[str]
    question: str
    answer: str
    explanation: str


def build_graph():
    sg = StateGraph(QAState)
    sg.add_node("research", researcher)
    sg.add_node("question", questioner)
    sg.add_node("answer", answerer)
    sg.add_node("review", reviewer)

    sg.set_entry_point("research")
    sg.add_edge("research", "question")
    sg.add_edge("question", "answer")
    sg.add_edge("answer", "review")
    sg.add_edge("review", END)
    return sg.compile()


COMP_GRAPH = build_graph()


def generate_exam(objectives: List[str], n: int = 5) -> List[Dict]:
    results = []
    for i in range(min(n, len(objectives))):
        state = {"objective": objectives[i]}
        qa = COMP_GRAPH.invoke(state)
        results.append({
            "objective": objectives[i],
            "question": qa.get("question", ""),
            "answer": qa.get("answer", ""),
            "explanation": qa.get("explanation", ""),
        })
    return results
