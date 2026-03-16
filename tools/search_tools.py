import os
from tavily import TavilyClient

def search_company_news(company_name: str) -> str:
    try:
        client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
        results = client.search(
            query=f"{company_name} stock news earnings latest 2025",
            max_results=5
        )
        news_text = ""
        for r in results["results"]:
            news_text += f"Title: {r['title']}\n"
            news_text += f"Summary: {r['content']}\n"
            news_text += f"Source: {r['url']}\n\n"
        return news_text
    except Exception as e:
        return f"News search error: {str(e)}"