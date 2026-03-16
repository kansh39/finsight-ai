import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_groq import ChatGroq
from schemas.models import AgentState

def report_agent(state: AgentState) -> AgentState:
    try:
        print("Report Agent: Generating investment report...")

        llm = ChatGroq(
            api_key=os.environ["GROQ_API_KEY"],
            model="llama-3.1-8b-instant"
        )

        financials = state["financials"]
        fin_text = f"""
Company: {financials.get('company_name', 'N/A')}
Ticker: {financials.get('ticker', 'N/A')}
Current Price: {financials.get('current_price', 'N/A')}
Market Cap: {financials.get('market_cap', 'N/A')}
P/E Ratio: {financials.get('pe_ratio', 'N/A')}
Revenue: {financials.get('revenue', 'N/A')}
Profit Margin: {financials.get('profit_margin', 'N/A')}
52 Week High: {financials.get('52w_high', 'N/A')}
52 Week Low: {financials.get('52w_low', 'N/A')}
EPS: {financials.get('eps', 'N/A')}
Sector: {financials.get('sector', 'N/A')}
Industry: {financials.get('industry', 'N/A')}
"""

        prompt = f"""You are a professional financial analyst. Write a detailed investment research report.

Company: {state['company']}

FINANCIAL DATA:
{fin_text}

RECENT NEWS:
{state['news']}

SENTIMENT ANALYSIS:
{state['sentiment']}

Write a complete investment report with these exact sections:

# {state['company']} Investment Research Report

## 1. Executive Summary
(3-4 sentences overview)

## 2. Company Overview
(Brief description of what the company does)

## 3. Financial Health
(Analyze the financial metrics provided)

## 4. Recent Developments
(Based on the news provided)

## 5. Sentiment Analysis
(Based on the sentiment data provided)

## 6. Key Risks
(3-4 bullet points)

## 7. Growth Opportunities
(3-4 bullet points)

## 8. Final Recommendation
(Buy / Hold / Sell with clear reasoning)"""

        result = llm.invoke(prompt)
        state["report"] = result.content
        print("Report Agent: Done!")
    except Exception as e:
        state["report"] = "Report generation failed."
        state["error"] = f"Report Agent error: {str(e)}"
    return state