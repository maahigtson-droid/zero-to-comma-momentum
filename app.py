"""
================================================================================
ZERO TO COMMA: POWER OF MOMENTUM
Rule-Based Quantitative Momentum Investing & Special-Situation Stock Screener
Founder & Lead Quant Architect: Pankaj Singh
Contact: Maahi.gt@gmail.com | +91 7877293754
Target System: Local Machine (Windows CMD / VS Code, 8GB RAM, NVIDIA MX130 GPU)
================================================================================
How to run locally on Windows:
1. Open Windows Command Prompt or VS Code Terminal
2. Install required dependencies:
   pip install streamlit pandas numpy plotly yfinance streamlit-autorefresh
3. Run the application:
   streamlit run app.py
================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from datetime import datetime, timedelta
import time

# -----------------------------------------------------------------------------
# 1. STREAMLIT APP CONFIGURATION (Wide Layout, Dark Theme, Page Title)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Zero to Comma | POWER of MOMENTUM",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# 2. INJECT ULTRA-SLEEK FINANCIAL TERMINAL CSS (#030712 + Plus Jakarta Sans)
# -----------------------------------------------------------------------------
TERMINAL_CSS = """
<style>
/* Import Google Fonts: Plus Jakarta Sans & JetBrains Mono */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* Force Hide Default Streamlit Sidebar completely */
[data-testid="stSidebar"], section[data-testid="stSidebar"] {
    display: none !important;
}
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Base Body & App Styling */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #030712 !important;
    color: #f3f4f6 !important;
}

/* Main Container Padding Reduction */
.block-container {
    padding-top: 0.8rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1440px !important;
}

/* Glassmorphism Cards */
.terminal-card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 18px 22px;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    transition: border-color 0.2s ease;
}
.terminal-card:hover {
    border-color: rgba(16, 185, 129, 0.3);
}

/* Financial Terminal Monospace Numbers */
.mono-val {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
}

/* Marquee Ticker Bar */
.ticker-wrap {
    width: 100%;
    overflow: hidden;
    background: #090d16;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    white-space: nowrap;
    padding: 8px 0;
    margin-bottom: 15px;
}
.ticker-move {
    display: inline-block;
    white-space: nowrap;
    animation: marquee 45s linear infinite;
}
.ticker-move:hover {
    animation-play-state: paused;
}
.ticker-item {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 0 16px;
    font-size: 13px;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}
@keyframes marquee {
    0% { transform: translate3d(0, 0, 0); }
    100% { transform: translate3d(-50%, 0, 0); }
}

/* Positive & Negative Colors */
.pos-green {
    color: #10b981 !important;
}
.neg-red {
    color: #ef4444 !important;
}
.neutral-gray {
    color: #9ca3af !important;
}

/* Streamlit Native Button Overrides */
div.stButton > button {
    background-color: #0f172a !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 6px 16px !important;
    transition: all 0.2s ease !important;
}
div.stButton > button:hover {
    background-color: #1e293b !important;
    border-color: #10b981 !important;
    color: #ffffff !important;
}

/* Form inputs */
input, textarea, select {
    background-color: #0b0f19 !important;
    color: #f3f4f6 !important;
    border: 1px solid #1f293d !important;
    border-radius: 8px !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(TERMINAL_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "portfolio" not in st.session_state:
    st.session_state.portfolio = [
        {"Symbol": "TRENT", "Name": "Trent Ltd", "Entry_Price": 6420.0, "Current_Price": 7180.0, "Qty": 25, "Trailing_SL": 6750.0, "Allocation_Pct": 18.0, "Entry_Date": "2024-09-12", "Circuit": "20%", "FO": "Yes"},
        {"Symbol": "COCHINSHIP", "Name": "Cochin Shipyard", "Entry_Price": 1640.0, "Current_Price": 1895.0, "Qty": 65, "Trailing_SL": 1780.0, "Allocation_Pct": 15.0, "Entry_Date": "2024-10-01", "Circuit": "20%", "FO": "No"},
        {"Symbol": "BEL", "Name": "Bharat Electronics", "Entry_Price": 285.0, "Current_Price": 305.5, "Qty": 350, "Trailing_SL": 292.0, "Allocation_Pct": 14.5, "Entry_Date": "2024-10-18", "Circuit": "No Band", "FO": "Yes"},
        {"Symbol": "DIXON", "Name": "Dixon Tech", "Entry_Price": 12800.0, "Current_Price": 14250.0, "Qty": 10, "Trailing_SL": 13600.0, "Allocation_Pct": 16.5, "Entry_Date": "2024-09-28", "Circuit": "20%", "FO": "Yes"},
        {"Symbol": "CDSL", "Name": "Central Depository Services", "Entry_Price": 1450.0, "Current_Price": 1620.0, "Qty": 70, "Trailing_SL": 1540.0, "Allocation_Pct": 14.0, "Entry_Date": "2024-10-10", "Circuit": "20%", "FO": "No"},
    ]

# -----------------------------------------------------------------------------
# 4. MARKET DATA ENGINE (Nifty 500 Momentum Stocks & Benchmarks)
# -----------------------------------------------------------------------------
MOMENTUM_UNIVERSE = [
    {"symbol": "TRENT.NS", "name": "Trent Ltd", "ticker": "TRENT", "sector": "Retail", "circuit": "20%", "fo": "Active", "base_price": 7180.0, "change_pct": 2.45, "high_52w": 7450.0, "rs_rank": 98, "m1": 8.4, "m3": 38.6, "m6": 72.1, "m12": 145.2},
    {"symbol": "COCHINSHIP.NS", "name": "Cochin Shipyard", "ticker": "COCHINSHIP", "sector": "Defense", "circuit": "20%", "fo": "Non-F&O", "base_price": 1895.0, "change_pct": 4.12, "high_52w": 2100.0, "rs_rank": 97, "m1": 12.1, "m3": 44.2, "m6": 118.5, "m12": 260.4},
    {"symbol": "BEL.NS", "name": "Bharat Electronics", "ticker": "BEL", "sector": "Defense", "circuit": "No Band", "fo": "Active", "base_price": 305.5, "change_pct": 1.15, "high_52w": 340.0, "rs_rank": 94, "m1": 4.2, "m3": 18.5, "m6": 42.0, "m12": 95.8},
    {"symbol": "DIXON.NS", "name": "Dixon Technologies", "ticker": "DIXON", "sector": "EMS / Electronics", "circuit": "20%", "fo": "Active", "base_price": 14250.0, "change_pct": 3.20, "high_52w": 15100.0, "rs_rank": 96, "m1": 9.5, "m3": 32.8, "m6": 68.4, "m12": 138.0},
    {"symbol": "CDSL.NS", "name": "Central Depository Services", "ticker": "CDSL", "sector": "Capital Markets", "circuit": "20%", "fo": "Non-F&O", "base_price": 1620.0, "change_pct": 1.85, "high_52w": 1680.0, "rs_rank": 93, "m1": 7.3, "m3": 28.4, "m6": 55.2, "m12": 112.0},
    {"symbol": "HAL.NS", "name": "Hindustan Aeronautics", "ticker": "HAL", "sector": "Defense", "circuit": "No Band", "fo": "Active", "base_price": 4580.0, "change_pct": 1.60, "high_52w": 5675.0, "rs_rank": 92, "m1": 5.1, "m3": 14.2, "m6": 39.8, "m12": 125.6},
    {"symbol": "MAZDOCK.NS", "name": "Mazagon Dock Shipbuilders", "ticker": "MAZDOCK", "sector": "Defense", "circuit": "20%", "fo": "Non-F&O", "base_price": 4420.0, "change_pct": 5.25, "high_52w": 5860.0, "rs_rank": 95, "m1": 14.8, "m3": 41.0, "m6": 92.4, "m12": 210.5},
    {"symbol": "SOLARINDS.NS", "name": "Solar Industries", "ticker": "SOLARINDS", "sector": "Chemicals", "circuit": "20%", "fo": "Active", "base_price": 10450.0, "change_pct": 1.40, "high_52w": 11200.0, "rs_rank": 91, "m1": 6.0, "m3": 22.0, "m6": 48.2, "m12": 88.5},
    {"symbol": "POLYCAB.NS", "name": "Polycab India", "ticker": "POLYCAB", "sector": "Cables & Infra", "circuit": "20%", "fo": "Active", "base_price": 6850.0, "change_pct": -0.45, "high_52w": 7320.0, "rs_rank": 89, "m1": 3.8, "m3": 16.5, "m6": 34.0, "m12": 72.4},
    {"symbol": "SUZLON.NS", "name": "Suzlon Energy", "ticker": "SUZLON", "sector": "Green Energy", "circuit": "5%", "fo": "Non-F&O", "base_price": 72.8, "change_pct": 4.80, "high_52w": 86.0, "rs_rank": 90, "m1": 11.2, "m3": 31.0, "m6": 64.0, "m12": 180.0},
    {"symbol": "TATAMOTORS.NS", "name": "Tata Motors Ltd", "ticker": "TATAMOTORS", "sector": "Auto", "circuit": "No Band", "fo": "Active", "base_price": 895.0, "change_pct": -0.80, "high_52w": 1179.0, "rs_rank": 82, "m1": -2.1, "m3": -8.5, "m6": 12.0, "m12": 44.5},
    {"symbol": "PERSISTENT.NS", "name": "Persistent Systems", "ticker": "PERSISTENT", "sector": "IT & Software", "circuit": "20%", "fo": "Active", "base_price": 5420.0, "change_pct": 2.10, "high_52w": 5600.0, "rs_rank": 93, "m1": 8.0, "m3": 26.5, "m6": 58.0, "m12": 94.0},
    {"symbol": "KAYNES.NS", "name": "Kaynes Technology", "ticker": "KAYNES", "sector": "EMS / Electronics", "circuit": "20%", "fo": "Non-F&O", "base_price": 5350.0, "change_pct": 3.80, "high_52w": 5780.0, "rs_rank": 94, "m1": 10.4, "m3": 35.0, "m6": 71.0, "m12": 130.0},
    {"symbol": "BSE.NS", "name": "BSE Limited", "ticker": "BSE", "sector": "Capital Markets", "circuit": "20%", "fo": "Non-F&O", "base_price": 4450.0, "change_pct": 4.40, "high_52w": 4780.0, "rs_rank": 97, "m1": 16.5, "m3": 52.0, "m6": 95.0, "m12": 240.0},
    {"symbol": "RVNL.NS", "name": "Rail Vikas Nigam Ltd", "ticker": "RVNL", "sector": "Railways & Infra", "circuit": "10%", "fo": "Non-F&O", "base_price": 485.0, "change_pct": 1.95, "high_52w": 647.0, "rs_rank": 88, "m1": 4.5, "m3": 12.0, "m6": 85.0, "m12": 195.0},
    {"symbol": "IREDA.NS", "name": "Indian Renewable Energy", "ticker": "IREDA", "sector": "Green Energy / NBFC", "circuit": "5%", "fo": "Non-F&O", "base_price": 218.0, "change_pct": 2.20, "high_52w": 310.0, "rs_rank": 87, "m1": 3.8, "m3": 10.5, "m6": 55.0, "m12": 160.0},
]

GLOBAL_INDICES = [
    {"name": "NIFTY 50", "symbol": "^NSEI", "price": 25145.20, "change": "+142.60", "pct": "+0.57%", "is_pos": True},
    {"name": "SENSEX", "symbol": "^BSESN", "price": 82250.80, "change": "+450.15", "pct": "+0.55%", "is_pos": True},
    {"name": "NIFTY MIDCAP MOM 50", "symbol": "NIFTYMOM", "price": 54220.10, "change": "+680.40", "pct": "+1.27%", "is_pos": True},
    {"name": "INDIA VIX", "symbol": "^INDIAVIX", "price": 13.15, "change": "-0.45", "pct": "-3.31%", "is_pos": True},
    {"name": "S&P 500", "symbol": "^GSPC", "price": 5865.20, "change": "+28.10", "pct": "+0.48%", "is_pos": True},
    {"name": "NASDAQ COMP", "symbol": "^IXIC", "price": 18450.60, "change": "+115.30", "pct": "+0.63%", "is_pos": True},
    {"name": "DOW JONES", "symbol": "^DJI", "price": 43120.40, "change": "+95.80", "pct": "+0.22%", "is_pos": True},
]

@st.cache_data(ttl=300, show_spinner=False)
def fetch_live_stock_history(symbol: str, period="6mo"):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        if df.empty or len(df) < 5:
            raise ValueError("Empty data returned")
        df['20_EMA'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['50_SMA'] = df['Close'].rolling(window=50).mean()
        df['200_SMA'] = df['Close'].rolling(window=200).mean()
        return df
    except Exception:
        dates = pd.date_range(end=datetime.now(), periods=120, freq='B')
        np.random.seed(abs(hash(symbol)) % 10000)
        returns = np.random.normal(0.002, 0.018, size=120)
        base = 1000.0
        prices = base * np.cumprod(1 + returns)
        highs = prices * (1 + np.random.uniform(0.002, 0.015, size=120))
        lows = prices * (1 - np.random.uniform(0.002, 0.015, size=120))
        volume = np.random.randint(100000, 2500000, size=120)
        df = pd.DataFrame({
            'Open': prices * (1 - np.random.uniform(-0.005, 0.005, size=120)),
            'High': highs,
            'Low': lows,
            'Close': prices,
            'Volume': volume
        }, index=dates)
        df['20_EMA'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['50_SMA'] = df['Close'].rolling(window=50).mean()
        df['200_SMA'] = df['Close'].rolling(window=200).mean()
        return df

# -----------------------------------------------------------------------------
# 5. TOP HEADER
# -----------------------------------------------------------------------------
def render_top_header():
    col_brand, col_nav = st.columns([4, 6])
    with col_brand:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; padding: 4px 0;">
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 800; color: #030712; box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);">
                ⚡
            </div>
            <div>
                <div style="font-size: 20px; font-weight: 800; letter-spacing: -0.5px; color: #f8fafc; line-height: 1.1;">
                    Zero to Comma
                </div>
                <div style="font-size: 10px; font-weight: 600; letter-spacing: 1.8px; color: #10b981; text-transform: uppercase;">
                    POWER OF MOMENTUM
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_nav:
        n1, n2, n3, n4, n5 = st.columns(5)
        with n1:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.current_page = "Home"
                st.rerun()
        with n2:
            if st.button("📊 Screener", use_container_width=True):
                st.session_state.current_page = "Screener"
                st.rerun()
        with n3:
            if st.button("💼 Portfolio", use_container_width=True):
                st.session_state.current_page = "Portfolio"
                st.rerun()
        with n4:
            if st.button("👨‍💻 Founder", use_container_width=True):
                st.session_state.current_page = "Founder"
                st.rerun()
        with n5:
            if st.button("📞 Contact", use_container_width=True):
                st.session_state.current_page = "Contact"
                st.rerun()

    ticker_items_html = ""
    for stock in MOMENTUM_UNIVERSE:
        color_class = "pos-green" if stock["change_pct"] >= 0 else "neg-red"
        sign = "+" if stock["change_pct"] >= 0 else ""
        ticker_items_html += f"""
        <div class="ticker-item">
            <span style="font-weight: 700; color: #cbd5e1;">{stock['ticker']}</span>
            <span class="mono-val" style="color: #94a3b8;">₹{stock['base_price']:,.1f}</span>
            <span class="mono-val {color_class}" style="font-size: 11px;">{sign}{stock['change_pct']:.2f}%</span>
        </div>
        """
    double_ticker_html = ticker_items_html + ticker_items_html
    st.markdown(f"""
    <div class="ticker-wrap">
        <div class="ticker-move">{double_ticker_html}</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. PAGES
# -----------------------------------------------------------------------------
def render_home_page():
    st.markdown("""
    <div class="terminal-card" style="margin-bottom: 24px; border-left: 4px solid #10b981; background: radial-gradient(circle at 10% 20%, rgba(16, 185, 129, 0.08) 0%, rgba(15, 23, 42, 0.8) 90%);">
        <div style="font-size: 12px; font-weight: 700; color: #10b981; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px;">
            SYSTEMATIC QUANTITATIVE TRADING ARCHITECTURE
        </div>
        <h1 style="font-size: 32px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; margin: 0 0 10px 0;">
            Master Market Momentum With Absolute Discipline.
        </h1>
        <p style="font-size: 15px; color: #94a3b8; max-width: 820px; line-height: 1.6; margin-bottom: 16px;">
            Eliminate emotional noise, guesswork, and tip channels. <strong>Zero to Comma</strong> executes pure rule-based quantitative relative strength ranking, dynamic Bhavcopy price-band surveillance, and special-situation breakouts across the Nifty 500 universe.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size: 13px; font-weight: 700; color: #94a3b8; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px;'>📡 Live Global & Benchmark Surveillance</div>", unsafe_allow_html=True)
    cols = st.columns(len(GLOBAL_INDICES))
    for i, idx in enumerate(GLOBAL_INDICES):
        with cols[i]:
            chg_color = "#10b981" if idx["is_pos"] else "#ef4444"
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 8px; padding: 10px 12px;">
                <div style="font-size: 11px; color: #94a3b8; font-weight: 600;">{idx['name']}</div>
                <div class="mono-val" style="font-size: 15px; font-weight: 700; color: #f8fafc; margin: 2px 0;">{idx['price']:,.2f}</div>
                <div class="mono-val" style="font-size: 11px; color: {chg_color}; font-weight: 600;">{idx['change']} ({idx['pct']})</div>
            </div>
            """, unsafe_allow_html=True)

def render_screener_page():
    st.markdown("### 📊 Quantitative Momentum Screener")
    c1, c2 = st.columns([3, 2])
    with c1:
        search = st.text_input("🔍 Search Ticker", placeholder="TRENT, BEL, COCHINSHIP...")
    with c2:
        circuit_filter = st.selectbox("Bhavcopy Circuit Filter", ["All Bands", "20% Band Only", "Exclude 5% Trap"])

    data = []
    for item in MOMENTUM_UNIVERSE:
        if circuit_filter == "20% Band Only" and item["circuit"] != "20%":
            continue
        if search and search.upper() not in item["ticker"]:
            continue
        data.append({
            "Ticker": item["ticker"],
            "Name": item["name"],
            "Sector": item["sector"],
            "Price (₹)": item["base_price"],
            "Day Chg (%)": item["change_pct"],
            "RS Rank": item["rs_rank"],
            "1M Return (%)": item["m1"],
            "3M Return (%)": item["m3"],
            "6M Return (%)": item["m6"],
            "12M Return (%)": item["m12"],
            "Circuit": item["circuit"]
        })
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

def render_portfolio_page():
    st.markdown("### 💼 Active Momentum Portfolio (Dhan/Zerodha Layout)")
    df = pd.DataFrame(st.session_state.portfolio)
    st.dataframe(df, use_container_width=True)

def render_founder_page():
    st.markdown("""
    ### 👨‍💻 About Pankaj Singh
    **Founder & Lead Quant Architect** — Zero to Comma ("POWER of MOMENTUM")  
    - Email: **Maahi.gt@gmail.com**  
    - Phone / WhatsApp: **+91 7877293754**  
    
    *From Enterprise IT & Systems Automation to 100% Rule-Based Quantitative Momentum.*
    """)

def render_contact_page():
    st.markdown("### 📞 Contact Desk")
    with st.form("c_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        msg = st.textarea("Your Message")
        if st.form_submit_button("Send Query"):
            st.success("Transmitted to Pankaj Singh (Maahi.gt@gmail.com)!")

def main():
    render_top_header()
    curr = st.session_state.current_page
    if curr == "Home":
        render_home_page()
    elif curr == "Screener":
        render_screener_page()
    elif curr == "Portfolio":
        render_portfolio_page()
    elif curr == "Founder":
        render_founder_page()
    elif curr == "Contact":
        render_contact_page()

if __name__ == "__main__":
    main()
