import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langgraph.graph import StateGraph, END
from schemas.models import AgentState
from agents.research_agent import research_agent
from agents.financial_agent import financial_agent
from agents.sentiment_agent import sentiment_agent
from agents.report_agent import report_agent

def create_workflow():
    graph = StateGraph(AgentState)

    graph.add_node("research", research_agent)
    graph.add_node("financial", financial_agent)
    graph.add_node("sentiment", sentiment_agent)
    graph.add_node("report", report_agent)

    graph.set_entry_point("research")
    graph.add_edge("research", "financial")
    graph.add_edge("financial", "sentiment")
    graph.add_edge("sentiment", "report")
    graph.add_edge("report", END)

    return graph.compile()

workflow = create_workflow()