import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.search_tools import search_company_news
from schemas.models import AgentState

def research_agent(state: AgentState) -> AgentState:
    try:
        company = state["company"]
        print(f"Research Agent: Searching news for {company}...")
        news = search_company_news(company)
        state["news"] = news
        print("Research Agent: Done!")
    except Exception as e:
        state["news"] = ""
        state["error"] = f"Research Agent error: {str(e)}"
    return state