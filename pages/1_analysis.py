import streamlit as st

st.set_page_config(page_title="Analysis | FinSight AI", page_icon="📊", layout="wide")

st.title("📊 How FinSight AI Works")
st.caption("Understanding the Multi-Agent System")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("What is Multi-Agent AI?")
    st.markdown("""
    FinSight AI uses **4 specialized AI agents** that work together:
    
    **1. Research Agent**
    - Searches the internet for latest company news
    - Uses Tavily Search API
    - Returns structured news summaries
    
    **2. Financial Agent**
    - Pulls live stock data using yfinance
    - Gets P/E ratio, revenue, profit margin
    - Returns real financial metrics
    
    **3. Sentiment Agent**
    - Reads news headlines
    - Scores sentiment as Bullish/Neutral/Bearish
    - Uses Groq LLaMA 3 AI model
    
    **4. Report Agent**
    - Combines all agent outputs
    - Writes a professional investment report
    - Gives Buy/Hold/Sell recommendation
    """)

with col2:
    st.subheader("Tech Stack")
    st.markdown("""
    | Technology | Purpose |
    |---|---|
    | LangGraph | Agent orchestration |
    | Groq LLaMA 3 | AI language model |
    | Tavily Search | Real-time web search |
    | yfinance | Live stock data |
    | Streamlit | Web dashboard |
    | Plotly | Interactive charts |
    | Python | Core language |
    """)

st.markdown("---")
st.subheader("Agent Workflow")
st.markdown("""
```
User Input (Company + Ticker)
        ↓
Research Agent → searches news
        ↓
Financial Agent → pulls stock data
        ↓
Sentiment Agent → analyzes news mood
        ↓
Report Agent → writes full report
        ↓
Dashboard shows results
```
""")