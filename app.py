import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import config
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import datetime
from fpdf import FPDF
from graph.workflow import workflow

st.set_page_config(
    page_title="FinSight AI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0D1B40, #00B4D8);
        padding: 20px 30px;
        border-radius: 12px;
        margin-bottom: 24px;
    }
    .main-header h1 { color: white; margin: 0; font-size: 2.2rem; }
    .main-header p { color: #90E0EF; margin: 4px 0 0; font-size: 1rem; }
    div[data-testid="stMetric"] {
        background: #1E2A3A;
        border: 1px solid #00B4D8;
        border-radius: 10px;
        padding: 12px 16px;
    }
div[data-testid="stMetric"] label {
        color: #90E0EF !important;
    }
div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>📈 FinSight AI</h1>
    <p>Multi-Agent Financial Research Assistant — Powered by LangGraph + Groq LLaMA 3</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### About FinSight AI")
    st.markdown("""
    FinSight AI uses **4 specialized AI agents**:
    - Research Agent
    - Financial Agent
    - Sentiment Agent
    - Report Agent
    """)
    st.markdown("---")
    st.markdown("### Tech Stack")
    st.markdown("""
    - LangGraph
    - Groq LLaMA 3
    - Tavily Search
    - Alpha Vantage
    - Streamlit
    """)
    st.markdown("---")
    st.caption("Built by Anshu Kumar | MSc Data Science")

st.markdown("### Search Company")

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    company = st.text_input("Company Name", placeholder="e.g. Tesla, Apple, Microsoft")
with col2:
    ticker = st.text_input("Stock Ticker", placeholder="e.g. TSLA, AAPL, MSFT")
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("Analyze", use_container_width=True)

st.markdown("**Quick select:**")
qcol1, qcol2, qcol3, qcol4 = st.columns(4)
if qcol1.button("Tesla"):
    st.session_state["company"] = "Tesla"
    st.session_state["ticker"] = "TSLA"
    st.session_state["do_analyze"] = True
    st.rerun()
if qcol2.button("Apple"):
    st.session_state["company"] = "Apple"
    st.session_state["ticker"] = "AAPL"
    st.session_state["do_analyze"] = True
    st.rerun()
if qcol3.button("Google"):
    st.session_state["company"] = "Google"
    st.session_state["ticker"] = "GOOGL"
    st.session_state["do_analyze"] = True
    st.rerun()
if qcol4.button("Microsoft"):
    st.session_state["company"] = "Microsoft"
    st.session_state["ticker"] = "MSFT"
    st.session_state["do_analyze"] = True
    st.rerun()

if "result" not in st.session_state:
    st.session_state["result"] = None

if analyze_btn and company and ticker:
    with st.spinner(f"Analyzing {company}... please wait 90 seconds..."):
        result = workflow.invoke({
            "company": company,
            "ticker": ticker.upper(),
            "news": "",
            "financials": {},
            "sentiment": "",
            "report": "",
            "error": None
        })
        st.session_state["result"] = result
        st.session_state["company"] = company
        st.session_state["ticker"] = ticker

result = st.session_state.get("result")
company = st.session_state.get("company", "")
ticker = st.session_state.get("ticker", "")

if result:
    st.success(f"Analysis complete for {company}!")
    st.markdown("---")

    fin = result.get("financials", {})

    st.markdown("### Key Financial Metrics")
    m1, m2, m3, m4, m5, m6 = st.columns(6)

    price = fin.get("current_price", "N/A")
    m1.metric("Current Price", f"${price}" if price != "N/A" else "N/A")

    pe = fin.get("pe_ratio", "N/A")
    m2.metric("P/E Ratio", round(pe, 2) if isinstance(pe, float) else pe)

    high = fin.get("52w_high", "N/A")
    m3.metric("52W High", f"${high}" if high != "N/A" else "N/A")

    low = fin.get("52w_low", "N/A")
    m4.metric("52W Low", f"${low}" if low != "N/A" else "N/A")

    eps = fin.get("eps", "N/A")
    m5.metric("EPS", eps)

    profit = fin.get("profit_margin", "N/A")
    if isinstance(profit, float):
        profit = f"{profit*100:.1f}%"
    m6.metric("Profit Margin", profit)

    m7, m8, m9, m10 = st.columns(4)
    market_cap = fin.get("market_cap", "N/A")
    if isinstance(market_cap, (int, float)):
        market_cap = f"${market_cap/1e9:.2f}B"
    m7.metric("Market Cap", market_cap)
    m8.metric("Sector", fin.get("sector", "N/A"))
    m9.metric("Industry", fin.get("industry", "N/A"))
    div = fin.get("dividend_yield", "N/A")
    if isinstance(div, float):
        div = f"{div*100:.2f}%"
    m10.metric("Dividend Yield", div)

    st.markdown("---")

    st.markdown(f"### {company} Stock Price — Last 1 Year")
    hist = fin.get("history")
    if hist is not None and not hist.empty:
        tab1, tab2 = st.tabs(["Line Chart", "Candlestick Chart"])
        with tab1:
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=hist.index,
                y=hist["Close"],
                mode="lines",
                name="Close Price",
                line=dict(color="#00B4D8", width=2),
                fill="tozeroy",
                fillcolor="rgba(0,180,216,0.1)"
            ))
            fig_line.update_layout(
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                height=400,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_line, use_container_width=True)
        with tab2:
            fig_candle = go.Figure(data=[go.Candlestick(
                x=hist.index,
                open=hist["Open"],
                high=hist["High"],
                low=hist["Low"],
                close=hist["Close"],
                increasing_line_color="#00FF88",
                decreasing_line_color="#FF4444"
            )])
            fig_candle.update_layout(
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                height=400,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_candle, use_container_width=True)
    else:
        st.info("Chart data not available for this ticker.")

    st.markdown("---")

    st.markdown("### Sentiment Analysis")
    sentiment = result.get("sentiment", "")
    if "Bullish" in sentiment:
        st.success(sentiment)
    elif "Bearish" in sentiment:
        st.error(sentiment)
    else:
        st.warning(sentiment)

    st.markdown("---")

    st.markdown("### Full Investment Report")
    st.markdown(result.get("report", "Report not available."))

    st.markdown("---")

    st.markdown("### Download Report")
    dcol1, dcol2 = st.columns(2)

    report_text = result.get("report", "")
    dcol1.download_button(
        label="Download as TXT",
        data=report_text,
        file_name=f"{company}_FinSight_Report.txt",
        mime="text/plain",
        use_container_width=True
    )

    try:
        class PDF(FPDF):
            def header(self):
                self.set_fill_color(13, 27, 64)
                self.rect(0, 0, 210, 22, "F")
                self.set_font("Helvetica", "B", 13)
                self.set_text_color(255, 255, 255)
                self.set_xy(10, 8)
                self.cell(190, 8, "FinSight AI - Investment Research Report", ln=True)
                self.set_text_color(0, 0, 0)

            def footer(self):
                self.set_y(-12)
                self.set_font("Helvetica", "I", 8)
                self.set_text_color(128, 128, 128)
                self.set_xy(10, -12)
                self.cell(190, 5, "FinSight AI | Not financial advice | Page " + str(self.page_no()), align="C")
                self.set_text_color(0, 0, 0)

        pdf = PDF()
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)
        pdf.set_auto_page_break(auto=True, margin=18)
        pdf.add_page()
        pw = 190

        pdf.ln(8)
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(13, 27, 64)
        pdf.set_x(10)
        pdf.multi_cell(pw, 9, company)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(0, 100, 180)
        pdf.set_x(10)
        pdf.multi_cell(pw, 6, "Ticker: " + ticker.upper() + "   |   Generated: " + datetime.datetime.now().strftime("%B %d, %Y"))
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)

        pdf.set_font("Helvetica", "B", 11)
        pdf.set_fill_color(13, 27, 64)
        pdf.set_text_color(255, 255, 255)
        pdf.set_x(10)
        pdf.cell(pw, 7, "  Key Financial Metrics", fill=True, ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(1)

        metrics = [
            ("Current Price", "$" + str(fin.get("current_price", "N/A"))),
            ("Market Cap", "$" + str(round(fin.get("market_cap", 0) / 1e9, 2)) + "B" if isinstance(fin.get("market_cap"), (int, float)) else "N/A"),
            ("P/E Ratio", str(round(fin.get("pe_ratio", 0), 2)) if isinstance(fin.get("pe_ratio"), float) else "N/A"),
            ("EPS", str(fin.get("eps", "N/A"))),
            ("52W High", "$" + str(fin.get("52w_high", "N/A"))),
            ("52W Low", "$" + str(fin.get("52w_low", "N/A"))),
            ("Profit Margin", str(round(fin.get("profit_margin", 0) * 100, 1)) + "%" if isinstance(fin.get("profit_margin"), float) else "N/A"),
            ("Sector", str(fin.get("sector", "N/A"))),
        ]

        cw = pw / 4
        for i in range(0, len(metrics), 2):
            pdf.set_x(10)
            bg = (240, 248, 255) if (i // 2) % 2 == 0 else (255, 255, 255)
            pdf.set_fill_color(*bg)
            label1, val1 = metrics[i]
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(cw, 6, " " + label1, border=1, fill=True)
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(cw, 6, " " + val1, border=1, fill=True)
            if i + 1 < len(metrics):
                label2, val2 = metrics[i + 1]
                pdf.set_font("Helvetica", "B", 9)
                pdf.cell(cw, 6, " " + label2, border=1, fill=True)
                pdf.set_font("Helvetica", "", 9)
                pdf.cell(cw, 6, " " + val2, border=1, fill=True)
            pdf.ln()
        pdf.ln(5)

        clean_text = report_text.encode("latin-1", "replace").decode("latin-1")
        for line in clean_text.split("\n"):
            line = line.strip()
            if not line:
                pdf.ln(2)
            elif line.startswith("##"):
                pdf.ln(2)
                pdf.set_fill_color(13, 27, 64)
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_x(10)
                pdf.cell(pw, 6, "  " + line.replace("#", "").strip(), fill=True, ln=True)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(1)
            elif line.startswith("#"):
                pdf.ln(3)
                pdf.set_fill_color(0, 100, 180)
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Helvetica", "B", 12)
                pdf.set_x(10)
                pdf.cell(pw, 7, "  " + line.replace("#", "").strip(), fill=True, ln=True)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(1)
            elif line.startswith("- ") or line.startswith("* "):
                pdf.set_font("Helvetica", "", 9)
                pdf.set_x(14)
                pdf.multi_cell(pw - 4, 5, "- " + line[2:])
            else:
                pdf.set_font("Helvetica", "", 9)
                pdf.set_x(10)
                pdf.multi_cell(pw, 5, line)

        pdf.ln(5)
        pdf.set_x(10)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(100, 70, 0)
        pdf.multi_cell(pw, 5, "DISCLAIMER: This report is generated by FinSight AI for informational purposes only. It does not constitute financial advice. Please consult a qualified financial advisor before making investment decisions.")
        pdf.set_text_color(0, 0, 0)

        pdf_bytes = bytes(pdf.output())
        dcol2.download_button(
            label="Download as PDF",
            data=pdf_bytes,
            file_name=f"{company}_FinSight_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        dcol2.error(f"PDF error: {str(e)}")
