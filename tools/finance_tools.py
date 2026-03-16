import yfinance as yf
import pandas as pd

def get_financial_data(ticker: str) -> dict:
    try:
        stock = yf.Ticker(ticker)
        
        # Force fresh download
        hist = stock.history(period="1y", auto_adjust=True)
        info = stock.info
        
        # Try fast_info as backup
        try:
            fast = stock.fast_info
            current_price = fast.last_price
        except Exception:
            current_price = info.get("currentPrice") or info.get("regularMarketPrice", "N/A")

        return {
            "ticker": ticker,
            "company_name": info.get("longName", ticker),
            "current_price": round(current_price, 2) if isinstance(current_price, float) else current_price,
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "revenue": info.get("totalRevenue", "N/A"),
            "profit_margin": info.get("profitMargins", "N/A"),
            "52w_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52w_low": info.get("fiftyTwoWeekLow", "N/A"),
            "eps": info.get("trailingEps", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "summary": info.get("longBusinessSummary", "N/A"),
            "history": hist
        }
    except Exception as e:
        return {"error": f"Financial data error: {str(e)}"}
