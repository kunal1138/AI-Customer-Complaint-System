"""
The LangGraph workflow definition.

Flow (mirrors the real QMS complaint intake process):

    extract -> completeness_check --(incomplete)--> END (flagged, returned to user)
                       |
                  (complete)
                       v
              duplicate_check
                       |
                       v
               risk_classification
                       |
                       v
              root_cause_and_capa
                       |
                       v
                   summary
                       |
                       v
                     END

Run `python -m app.agents.graph` to print a visual representation of this
graph (useful for the demo video walkthrough).
"""
from langgraph.graph import StateGraph, END
from app.agents.state import ComplaintState
from app.agents.nodes import (
    extract_complaint_data,
    check_completeness,
    check_duplicates,
    classify_risk,
    suggest_root_cause,
    generate_summary,
)


def route_after_completeness(state: ComplaintState) -> str:
    """Conditional edge: stop early if the complaint is missing critical fields,
    instead of wasting LLM calls on risk/CAPA analysis for incomplete data."""
    if state.get("completeness_status") == "Incomplete":
        return "end_incomplete"
    return "continue"


def build_complaint_graph():
    graph = StateGraph(ComplaintState)

    graph.add_node("extract", extract_complaint_data)
    graph.add_node("completeness_check", check_completeness)
    graph.add_node("duplicate_check", check_duplicates)
    graph.add_node("risk_classification", classify_risk)
    graph.add_node("root_cause_capa", suggest_root_cause)
    graph.add_node("summary", generate_summary)

    graph.set_entry_point("extract")
    graph.add_edge("extract", "completeness_check")

    graph.add_conditional_edges(
        "completeness_check",
        route_after_completeness,
        {
            "end_incomplete": END,
            "continue": "duplicate_check",
        },
    )

    graph.add_edge("duplicate_check", "risk_classification")
    graph.add_edge("risk_classification", "root_cause_capa")
    graph.add_edge("root_cause_capa", "summary")
    graph.add_edge("summary", END)

    return graph.compile()


complaint_graph = build_complaint_graph()


if __name__ == "__main__":
    # Prints an ASCII graph representation — screenshot this for your demo video
    # to show the LangGraph structure alongside your code walkthrough.
    print(complaint_graph.get_graph().draw_ascii())
