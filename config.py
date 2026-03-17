import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "YDIOQ269XP22HKZ4")
POLYGON_KEY = os.environ.get("POLYGON_KEY", "ibW5SHopeGVDEV69FD4s2FlIDGJ_Wzpl")

os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
os.environ["ALPHA_VANTAGE_KEY"] = ALPHA_VANTAGE_KEY
os.environ["POLYGON_KEY"] = POLYGON_KEY
