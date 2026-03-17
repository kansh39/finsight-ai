# 📈 FinSight AI — Multi-Agent Financial Research Assistant

> An autonomous AI system that researches any company in 30 seconds using 4 specialized AI agents — powered by LangGraph, Groq LLaMA 3, Polygon API, and Streamlit.

🔗 **Live Demo:** [finsight-ai-npuuxr7vrgckekl7msbmz3.streamlit.app](https://finsight-ai-npuuxr7vrgckekl7msbmz3.streamlit.app)

---

## 🚀 What is FinSight AI?

FinSight AI is an **agentic AI system** where you type a company name and 4 specialized AI agents automatically:

1. **Search** the internet for latest company news
2. **Pull** live stock data and financial metrics
3. **Analyze** market sentiment from news headlines
4. **Generate** a complete professional investment report

All in under 30 seconds. No human involved.

---

## 🤖 The 4 AI Agents

| Agent | Role | Technology |
|-------|------|------------|
| Research Agent | Searches latest news about the company | Tavily Search API |
| Financial Agent | Pulls live stock price, P/E ratio, revenue, market cap | Polygon.io API |
| Sentiment Agent | Scores news as Bullish / Neutral / Bearish | Groq LLaMA 3 |
| Report Agent | Writes full investment report with recommendation | Groq LLaMA 3 |

The **Orchestrator** (LangGraph StateGraph) coordinates all agents — decides what runs, in what order, and combines results.

---

## ✨ Features

- 🧠 **Multi-Agent Architecture** — LangGraph StateGraph orchestrating 4 specialized agents
- 📊 **Live Financial Data** — Real-time stock prices, P/E ratio, market cap, EPS via Polygon API
- 🌐 **Live Web Search** — Latest company news via Tavily Search
- 🎯 **Sentiment Analysis** — Bullish / Neutral / Bearish scoring with key themes
- 📈 **Interactive Charts** — Line chart and Candlestick chart for 1 year price history
- 📋 **Full Investment Report** — Executive summary, risks, opportunities, Buy/Hold/Sell recommendation
- 📄 **PDF + TXT Download** — Download the generated report
- ⚡ **Concise / Detailed Modes** — Toggle response length
- 💬 **AI Chat Page** — Ask follow-up questions about stocks and finance

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **LangGraph** | Multi-agent orchestration (StateGraph) |
| **Groq LLaMA 3** | Fast LLM inference for sentiment + report generation |
| **Tavily Search** | Real-time web search for company news |
| **Polygon.io API** | Live stock data and price history |
| **Streamlit** | Interactive web dashboard |
| **Plotly** | Interactive stock charts |
| **LangChain** | LLM integration and agent tools |
| **Python** | Core language |

---

## 📁 Project Structure

```
finsight-ai/
├── agents/
│   ├── research_agent.py      ← Searches latest company news
│   ├── financial_agent.py     ← Pulls live stock data
│   ├── sentiment_agent.py     ← Analyzes news sentiment
│   └── report_agent.py        ← Generates investment report
├── graph/
│   └── workflow.py            ← LangGraph StateGraph orchestrator
├── tools/
│   ├── search_tools.py        ← Tavily web search
│   └── finance_tools.py       ← Polygon API integration
├── schemas/
│   └── models.py              ← AgentState TypedDict
├── pages/
│   ├── 1_analysis.py          ← How it works page
│   └── 2_chat.py              ← AI financial chat
├── app.py                     ← Main Streamlit dashboard
├── config.py                  ← API key configuration
└── requirements.txt
```

---

## ⚙️ Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/kansh39/finsight-ai.git
cd finsight-ai

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate      # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add API keys to config.py
GROQ_API_KEY = "your_groq_key"
TAVILY_API_KEY = "your_tavily_key"
POLYGON_KEY = "your_polygon_key"

# 5. Run
streamlit run app.py
```

---

## 🔑 API Keys Required

| API | Where to Get | Cost |
|-----|-------------|------|
| Groq API | [console.groq.com](https://console.groq.com) | Free |
| Tavily Search | [app.tavily.com](https://app.tavily.com) | Free (1000/month) |
| Polygon.io | [polygon.io](https://polygon.io) | Free tier available |

---

## 🌐 Deployment

Deployed on **Streamlit Cloud**:
1. Push code to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect repo → set main file: `app.py`
4. Add secrets: `GROQ_API_KEY`, `TAVILY_API_KEY`, `POLYGON_KEY`
5. Deploy

---

## 👨‍💻 Built By

**Anshu Kumar** — MSc Data Science, Christ University Bangalore

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/anshuk674)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/kansh39)

---

## ⚠️ Disclaimer

FinSight AI is built for educational and demonstration purposes only. It does not constitute financial advice. Always consult a qualified financial advisor before making investment decisions.
