import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "YDIOQ269XP22HKZ4")

os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
os.environ["ALPHA_VANTAGE_KEY"] = ALPHA_VANTAGE_KEY
