import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_groq import ChatGroq
from schemas.models import AgentState

def sentiment_agent(state: AgentState) -> AgentState:
    try:
        print("Sentiment Agent: Analyzing news sentiment...")
        news = state["news"]
        
        if not news:
            state["sentiment"] = "No news available for sentiment analysis."
            return state

        llm = ChatGroq(
            api_key=os.environ["GROQ_API_KEY"],
            model="llama-3.1-8b-instant"
        )

        prompt = f"""Analyze the sentiment of these news headlines and summaries about a company.
        
News:
{news}

Return your analysis in this exact format:
SENTIMENT: Bullish/Neutral/Bearish
SCORE: (0-100, where 100 is most bullish)
POSITIVES:
- point 1
- point 2
- point 3
NEGATIVES:
- point 1
- point 2
- point 3
SUMMARY: (2 sentences explaining overall sentiment)"""

        result = llm.invoke(prompt)
        state["sentiment"] = result.content
        print("Sentiment Agent: Done!")
    except Exception as e:
        state["sentiment"] = "Sentiment analysis unavailable."
        state["error"] = f"Sentiment Agent error: {str(e)}"
    return state