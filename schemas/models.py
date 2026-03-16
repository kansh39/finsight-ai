from typing import TypedDict, Optional
import pandas as pd

class AgentState(TypedDict):
    company: str
    ticker: str
    news: str
    financials: dict
    sentiment: str
    report: str
    error: Optional[str]