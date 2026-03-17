import requests
import pandas as pd
from datetime import datetime, timedelta

POLYGON_KEY = "ibW5SHopeGVDEV69FD4s2FlIDGJ_Wzpl"

def get_financial_data(ticker: str) -> dict:
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

        # Call 1 - Company details
        detail_url = f"https://api.polygon.io/v3/reference/tickers/{ticker}?apiKey={POLYGON_KEY}"
        detail_data = requests.get(detail_url, timeout=15).json()
        detail = detail_data.get("results", {})

        # Call 2 - Previous day quote
        quote_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?apiKey={POLYGON_KEY}"
        quote_data = requests.get(quote_url, timeout=15).json()
        quote = quote_data.get("results", [{}])[0] if quote_data.get("results") else {}

        # Call 3 - Historical prices
        hist_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{year_ago}/{today}?adjusted=true&sort=asc&limit=365&apiKey={POLYGON_KEY}"
        hist_data = requests.get(hist_url, timeout=15).json()

        # Build price history dataframe
        hist = pd.DataFrame()
        if hist_data.get("results"):
            rows = []
            for d in hist_data["results"]:
                rows.append({
                    "Date": datetime.fromtimestamp(d["t"] / 1000),
                    "Open": d.get("o", 0),
                    "High": d.get("h", 0),
                    "Low": d.get("l", 0),
                    "Close": d.get("c", 0),
                    "Volume": d.get("v", 0)
                })
            if rows:
                hist = pd.DataFrame(rows).set_index("Date").sort_index()

        # Get ticker snapshot for more data
        snap_url = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers/{ticker}?apiKey={POLYGON_KEY}"
        snap_data = requests.get(snap_url, timeout=15).json()
        snap = snap_data.get("ticker", {})
        day = snap.get("day", {})
        prev_day = snap.get("prevDay", {})

        current_price = round(float(quote.get("c", 0)), 2) if quote.get("c") else "N/A"

        # Get financials
        fin_url = f"https://api.polygon.io/vX/reference/financials?ticker={ticker}&limit=1&apiKey={POLYGON_KEY}"
        fin_data = requests.get(fin_url, timeout=15).json()
        financials = fin_data.get("results", [{}])[0] if fin_data.get("results") else {}
        income = financials.get("financials", {}).get("income_statement", {})
        balance = financials.get("financials", {}).get("balance_sheet", {})

        revenue = income.get("revenues", {}).get("value", "N/A")
        net_income = income.get("net_income_loss", {}).get("value", "N/A")

        profit_margin = "N/A"
        if revenue not in ("N/A", 0) and net_income not in ("N/A", 0):
            try:
                profit_margin = round(float(net_income) / float(revenue), 4)
            except Exception:
                profit_margin = "N/A"

        # 52 week high/low from history
        week52_high = "N/A"
        week52_low = "N/A"
        if not hist.empty:
            week52_high = round(hist["High"].max(), 2)
            week52_low = round(hist["Low"].min(), 2)

        market_cap = detail.get("market_cap", "N/A")
        sector = detail.get("sic_description", "N/A")
        industry = detail.get("sic_description", "N/A")
        name = detail.get("name", ticker)
        description = detail.get("description", "N/A")

        return {
            "ticker": ticker,
            "company_name": name,
            "current_price": current_price,
            "market_cap": int(market_cap) if isinstance(market_cap, (int, float)) else "N/A",
            "pe_ratio": "N/A",
            "revenue": int(revenue) if isinstance(revenue, (int, float)) else "N/A",
            "profit_margin": profit_margin,
            "52w_high": week52_high,
            "52w_low": week52_low,
            "eps": "N/A",
            "dividend_yield": "N/A",
            "sector": sector,
            "industry": industry,
            "summary": description,
            "history": hist
        }

    except Exception as e:
        return {"error": f"Financial data error: {str(e)}"}
