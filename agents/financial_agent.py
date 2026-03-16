import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.finance_tools import get_financial_data
from schemas.models import AgentState

def financial_agent(state: AgentState) -> AgentState:
    try:
        ticker = state["ticker"]
        print(f"Financial Agent: Pulling data for {ticker}...")
        financials = get_financial_data(ticker)
        state["financials"] = financials
        print("Financial Agent: Done!")
    except Exception as e:
        state["financials"] = {}
        state["error"] = f"Financial Agent error: {str(e)}"
    return state