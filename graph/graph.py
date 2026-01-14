# graph/graph.py
from langgraph.graph import StateGraph, START, END
from schemas.state import GraphState

from graph.nodes.intent_node import intent_node
from graph.nodes.default_answer_node import default_answer_node
from graph.nodes.site_brief_node import site_brief_node
from graph.nodes.html_node import html_node
from graph.nodes.css_node import css_node
from graph.nodes.js_node import js_node
from graph.nodes.review_node import review_node
from graph.nodes.response_compose_node import response_compose_node


def build_graph():
    g = StateGraph(GraphState)

    g.add_node("intent", intent_node)
    g.add_node("default_answer", default_answer_node)

    g.add_node("site_brief", site_brief_node)
    g.add_node("html", html_node)
    g.add_node("css", css_node)
    g.add_node("js", js_node)
    g.add_node("review", review_node)

    g.add_node("response_compose", response_compose_node)

    g.add_edge(START, "intent")

    def route_from_intent(state: GraphState) -> str:
        return "build" if state.build_site else "default"

    g.add_conditional_edges(
        "intent",
        route_from_intent,
        {
            "build": "site_brief",
            "default": "default_answer",
        },
    )

    g.add_edge("site_brief", "html")
    g.add_edge("html", "css")
    g.add_edge("css", "js")
    g.add_edge("js", "review")
    g.add_edge("review", "response_compose")

    g.add_edge("default_answer", "response_compose")
    g.add_edge("response_compose", END)

    return g.compile()
