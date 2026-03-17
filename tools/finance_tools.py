import time
import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = "YDIOQ269XP22HKZ4"

def get_financial_data(ticker: str) -> dict:
    try:
        # Call 1 - Current price first
        quote_url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}"
        quote_data = requests.get(quote_url, timeout=15).json()
        time.sleep(13)

        # Call 2 - Overview
        overview_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}"
        overview = requests.get(overview_url, timeout=15).json()
        time.sleep(13)

        # Call 3 - Weekly history
        weekly_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={ticker}&apikey={API_KEY}"
        weekly_data = requests.get(weekly_url, timeout=15).json()

        # Parse current price
        current_price = "N/A"
        quote = quote_data.get("Global Quote", {})
        if quote:
            price_str = quote.get("05. price", "N/A")
            if price_str not in ("N/A", ""):
                current_price = round(float(price_str), 2)

        # Parse history
        hist = pd.DataFrame()
        if "Weekly Time Series" in weekly_data:
            ts = weekly_data["Weekly Time Series"]
            cutoff = datetime.now() - timedelta(days=365)
            rows = []
            for date_str, values in ts.items():
                date = datetime.strptime(date_str, "%Y-%m-%d")
                if date >= cutoff:
                    rows.append({
                        "Date": date,
                        "Open": float(values["1. open"]),
                        "High": float(values["2. high"]),
                        "Low": float(values["3. low"]),
                        "Close": float(values["4. close"]),
                        "Volume": float(values["5. volume"])
                    })
            if rows:
                hist = pd.DataFrame(rows).set_index("Date").sort_index()

        def safe_float(val):
            try:
                if val in (None, "N/A", "None", "", "-"):
                    return "N/A"
                return round(float(val), 2)
            except Exception:
                return "N/A"

        def safe_int(val):
            try:
                if val in (None, "N/A", "None", "", "-"):
                    return "N/A"
                return int(val)
            except Exception:
                return "N/A"

        return {
            "ticker": ticker,
            "company_name": overview.get("Name", ticker),
            "current_price": current_price,
            "market_cap": safe_int(overview.get("MarketCapitalization")),
            "pe_ratio": safe_float(overview.get("PERatio")),
            "revenue": safe_int(overview.get("RevenueTTM")),
            "profit_margin": safe_float(overview.get("ProfitMargin")),
            "52w_high": overview.get("52WeekHigh", "N/A"),
            "52w_low": overview.get("52WeekLow", "N/A"),
            "eps": safe_float(overview.get("EPS")),
            "dividend_yield": safe_float(overview.get("DividendYield")),
            "sector": overview.get("Sector", "N/A"),
            "industry": overview.get("Industry", "N/A"),
            "summary": overview.get("Description", "N/A"),
            "history": hist
        }

    except Exception as e:
        return {"error": f"Financial data error: {str(e)}"}
