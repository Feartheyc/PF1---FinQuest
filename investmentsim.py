import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils import t

# ==========================================
# 1. MARKET STOCKS DATA & FUNDAMENTALS
# ==========================================
STOCK_DATA = {
    "RELIANCE": {
        "name": "Reliance Industries Ltd",
        "sector": "Energy & Conglomerate",
        "base_price": 2940.0,
        "volatility": 0.015,
        "pe_ratio": 26.4,
        "market_cap": "₹19.8 Lakh Cr",
        "high_52w": 3024.90,
        "low_52w": 2220.30,
        "desc": "Energy, telecom, and retail conglomerate. Blue-chip defensive holding."
    },
    "TCS": {
        "name": "Tata Consultancy Services",
        "sector": "IT Services",
        "base_price": 3880.0,
        "volatility": 0.012,
        "pe_ratio": 29.8,
        "market_cap": "₹14.1 Lakh Cr",
        "high_52w": 4254.75,
        "low_52w": 3310.00,
        "desc": "Global IT consulting giant. Steady cash flows and regular dividend yield."
    },
    "HDFCBANK": {
        "name": "HDFC Bank Ltd",
        "sector": "Private Banking",
        "base_price": 1640.0,
        "volatility": 0.014,
        "pe_ratio": 18.2,
        "market_cap": "₹12.5 Lakh Cr",
        "high_52w": 1757.50,
        "low_52w": 1363.55,
        "desc": "Largest private sector bank in India. Strong credit growth, low NPA."
    },
    "INFY": {
        "name": "Infosys Ltd",
        "sector": "IT & Cloud",
        "base_price": 1490.0,
        "volatility": 0.018,
        "pe_ratio": 24.1,
        "market_cap": "₹6.2 Lakh Cr",
        "high_52w": 1620.00,
        "low_52w": 1355.00,
        "desc": "Software and cloud solutions. Sensitive to US interest rate expectations."
    },
    "TATAMOTORS": {
        "name": "Tata Motors Ltd",
        "sector": "Automobile & EV",
        "base_price": 965.0,
        "volatility": 0.024,
        "pe_ratio": 16.7,
        "market_cap": "₹3.5 Lakh Cr",
        "high_52w": 1065.60,
        "low_52w": 615.00,
        "desc": "EV passenger market leader and commercial vehicle manufacturer. High beta."
    },
    "ZOMATO": {
        "name": "Zomato Ltd",
        "sector": "Quick Commerce & Tech",
        "base_price": 185.0,
        "volatility": 0.035,
        "pe_ratio": 92.4,
        "market_cap": "₹1.6 Lakh Cr",
        "high_52w": 207.20,
        "low_52w": 98.40,
        "desc": "Blinkit quick-commerce hypergrowth stock. High volatility, momentum-driven."
    }
}

# ==========================================
# 2. SYNTHETIC PRICE HISTORY GENERATOR
# ==========================================
@st.cache_data(show_spinner=False)
def generate_stock_history(symbol, timeframe):
    stock = STOCK_DATA.get(symbol, STOCK_DATA["RELIANCE"])
    base = stock["base_price"]
    vol = stock["volatility"]
    
    seed = (hash(symbol) + hash(timeframe)) % (2**32)
    rng = np.random.default_rng(seed)
    now = datetime.now()

    if timeframe == "1D":
        periods = 75
        times = [now - timedelta(minutes=5 * (periods - i)) for i in range(periods)]
        noise = rng.normal(0, vol * 0.25, periods)
        trend = np.linspace(-0.005, 0.012, periods)
        prices = base * np.cumprod(1 + noise + trend / periods)
        
    elif timeframe == "1W":
        periods = 35
        times = [now - timedelta(hours=2 * (periods - i)) for i in range(periods)]
        noise = rng.normal(0, vol * 0.6, periods)
        trend = np.linspace(-0.015, 0.025, periods)
        prices = (base * 0.98) * np.cumprod(1 + noise + trend / periods)

    elif timeframe == "1M":
        periods = 30
        times = [now - timedelta(days=periods - i) for i in range(periods)]
        noise = rng.normal(0, vol, periods)
        trend = np.linspace(-0.03, 0.045, periods)
        prices = (base * 0.96) * np.cumprod(1 + noise + trend / periods)

    elif timeframe == "1Y":
        periods = 250
        times = [now - timedelta(days=int((periods - i) * 1.45)) for i in range(periods)]
        noise = rng.normal(0.0004, vol, periods)
        prices = (base * 0.78) * np.cumprod(1 + noise)

    else:  # "ALL"
        periods = 500
        times = [now - timedelta(days=int((periods - i) * 2.8)) for i in range(periods)]
        noise = rng.normal(0.0005, vol * 1.1, periods)
        prices = (base * 0.45) * np.cumprod(1 + noise)

    prices = prices * (base / prices[-1])
    
    df = pd.DataFrame({"Date": times, "Price": np.round(prices, 2)})
    df["MA20"] = df["Price"].rolling(window=min(20, len(df)), min_periods=1).mean()
    return df

# ==========================================
# 3. INTERACTIVE CHART BUILDER
# ==========================================
def render_stock_chart(symbol, timeframe):
    stock = STOCK_DATA[symbol]
    df = generate_stock_history(symbol, timeframe)
    
    start_price = df["Price"].iloc[0]
    latest_price = df["Price"].iloc[-1]
    pct_change = ((latest_price - start_price) / start_price) * 100
    is_positive = pct_change >= 0

    line_color = "#22c55e" if is_positive else "#ef4444"
    fill_color = "rgba(34, 197, 94, 0.12)" if is_positive else "rgba(239, 68, 68, 0.12)"

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=df["Price"],
        mode="lines",
        line=dict(color=line_color, width=2.5),
        fill="tozeroy",
        fillcolor=fill_color,
        name="Price",
        hovertemplate="<b>%{x|%d %b %Y, %H:%M}</b><br>Price: ₹%{y:,.2f}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=df["MA20"],
        mode="lines",
        line=dict(color="rgba(250, 204, 21, 0.6)", width=1.5, dash="dot"),
        name="MA (20)",
        hoverinfo="skip"
    ))

    fig.update_layout(
        height=360,
        margin=dict(l=10, r=10, t=15, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        hovermode="x unified",
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.05)",
            showline=False,
            zeroline=False,
            tickfont=dict(color="#94a3b8", size=10)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.05)",
            showline=False,
            zeroline=False,
            side="right",
            tickprefix="₹",
            tickfont=dict(color="#94a3b8", size=10)
        )
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    sign = "+" if is_positive else ""
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.03); padding:10px 16px; border-radius:12px; border:1px solid rgba(255,255,255,0.06); margin-bottom:15px;">
        <div>
            <span style="font-size:0.75rem; color:#94a3b8; text-transform:uppercase;">Current Price</span><br>
            <span style="font-size:1.3rem; font-weight:800; color:#f8fafc;">₹{latest_price:,.2f}</span>
            <span style="font-size:0.85rem; font-weight:700; color:{line_color}; margin-left:8px;">{sign}{pct_change:.2f}% ({timeframe})</span>
        </div>
        <div style="display:flex; gap:20px; text-align:right;">
            <div>
                <span style="font-size:0.7rem; color:#94a3b8;">52W HIGH</span><br>
                <span style="font-size:0.85rem; font-weight:700; color:#cbd5e1;">₹{stock['high_52w']:,}</span>
            </div>
            <div>
                <span style="font-size:0.7rem; color:#94a3b8;">52W LOW</span><br>
                <span style="font-size:0.85rem; font-weight:700; color:#cbd5e1;">₹{stock['low_52w']:,}</span>
            </div>
            <div>
                <span style="font-size:0.7rem; color:#94a3b8;">P/E RATIO</span><br>
                <span style="font-size:0.85rem; font-weight:700; color:#facc15;">{stock['pe_ratio']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 4. MAIN SIMULATOR UI
# ==========================================
def render_investmentsim():
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = {sym: 0 for sym in STOCK_DATA}
    if "selected_timeframe" not in st.session_state:
        st.session_state.selected_timeframe = "1M"

    p = st.session_state.get("game", {})
    available_cash = st.session_state.get("cash", float(p.get("investments", 1000)))

    # Header Bar
    top_col1, top_col2 = st.columns([3, 1])
    with top_col1:
        st.markdown(f"## 🏛️ {t('NSE Stock Exchange Terminal')}")
        st.caption(f"Trading as **{p.get('persona', 'Investor')}** | Cash Available for Investing: **₹{available_cash:,.2f}**")
    with top_col2:
        if st.button(f"🗺️ {t('Exit to Map')}", use_container_width=True, type="secondary"):
            if "game" in st.session_state:
                st.session_state.game["investments"] = int(available_cash)
                st.session_state.game["state"] = "MAP"
            st.rerun()

    st.markdown("<hr style='border-color: rgba(255,255,255,0.08); margin: 10px 0 20px 0;'>", unsafe_allow_html=True)

    col_chart, col_trade = st.columns([2.2, 1.2], gap="large")

    with col_chart:
        selected_symbol = st.selectbox(
            "Select Stock to Analyze",
            options=list(STOCK_DATA.keys()),
            format_func=lambda s: f"{s} — {STOCK_DATA[s]['name']} ({STOCK_DATA[s]['sector']})",
            label_visibility="collapsed"
        )
        selected_stock = STOCK_DATA[selected_symbol]

        # Targeted CSS to give timeframe buttons comfortable padding and prevent text wrapping
        st.markdown("""
        <style>
            div[data-testid="column"] .timeframe-btn button {
                padding: 6px 12px !important;
                min-width: 65px !important;
                font-size: 0.85rem !important;
                letter-spacing: 0.5px !important;
                white-space: nowrap !important;
            }
        </style>
        """, unsafe_allow_html=True)

        # Balanced columns with enough width so '1D', '1W', '1M', '1Y', 'ALL' don't truncate
        tf_cols = st.columns([1.8, 1.8, 1.8, 1.8, 1.8, 4])
        for idx, tf in enumerate(["1D", "1W", "1M", "1Y", "ALL"]):
            with tf_cols[idx]:
                st.markdown('<div class="timeframe-btn">', unsafe_allow_html=True)
                is_active = (st.session_state.selected_timeframe == tf)
                btn_type = "primary" if is_active else "secondary"
                if st.button(tf, key=f"tf_{tf}", use_container_width=True, type=btn_type):
                    st.session_state.selected_timeframe = tf
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        render_stock_chart(selected_symbol, st.session_state.selected_timeframe)

        st.markdown(f"""
        <div style="background:rgba(15,23,42,0.6); padding:14px 18px; border-radius:12px; border:1px solid rgba(255,255,255,0.06); font-size:0.85rem; color:#94a3b8; line-height:1.5;">
            <b style="color:#f8fafc;">Sector:</b> {selected_stock['sector']} &nbsp;|&nbsp; 
            <b style="color:#f8fafc;">Market Cap:</b> {selected_stock['market_cap']}<br>
            <span style="color:#cbd5e1;">{selected_stock['desc']}</span>
        </div>
        """, unsafe_allow_html=True)

    with col_trade:
        curr_price = selected_stock["base_price"]
        held_qty = st.session_state.portfolio.get(selected_symbol, 0)

        st.markdown(f"### ⚡ {t('Order Execution')}")
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02); padding:12px; border-radius:10px; margin-bottom:14px; font-size:0.85rem;">
            You own: <b style="color:#67e8f9;">{held_qty} shares</b><br>
            Holding value: <b style="color:#4ade80;">₹{held_qty * curr_price:,.2f}</b>
        </div>
        """, unsafe_allow_html=True)

        qty = st.number_input("Shares Quantity", min_value=1, max_value=1000, value=1, step=1)
        total_order_cost = qty * curr_price

        st.markdown(f"Total Order Value: **₹{total_order_cost:,.2f}**")

        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button("🟢 BUY", use_container_width=True, type="primary"):
                if available_cash >= total_order_cost:
                    st.session_state.cash = available_cash - total_order_cost
                    st.session_state.portfolio[selected_symbol] = held_qty + qty
                    st.toast(f"Bought {qty} shares of {selected_symbol}!", icon="✅")
                    st.rerun()
                else:
                    st.error("Insufficient Cash!")

        with b_c2:
            if st.button("🔴 SELL", use_container_width=True):
                if held_qty >= qty:
                    st.session_state.cash = available_cash + total_order_cost
                    st.session_state.portfolio[selected_symbol] = held_qty - qty
                    st.toast(f"Sold {qty} shares of {selected_symbol}!", icon="💰")
                    st.rerun()
                else:
                    st.error("Not enough shares to sell!")

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        st.markdown(f"#### 📊 {t('Holdings')}")

        holdings_data = []
        total_holding_val = 0.0

        for sym, q in st.session_state.portfolio.items():
            if q > 0:
                p_val = q * STOCK_DATA[sym]["base_price"]
                total_holding_val += p_val
                holdings_data.append({"Stock": sym, "Qty": q, "Value (₹)": f"₹{p_val:,.0f}"})

        if holdings_data:
            st.dataframe(pd.DataFrame(holdings_data), use_container_width=True, hide_index=True)
        else:
            st.caption("No active holdings in portfolio.")

        net_terminal_worth = available_cash + total_holding_val
        st.markdown(f"""
        <div style="background:rgba(56,189,248,0.06); border:1px solid rgba(56,189,248,0.2); padding:10px 14px; border-radius:10px; margin-top:10px; font-size:0.88rem; text-align:center;">
            Total Portfolio Net Worth: <b style="color:#38bdf8;">₹{net_terminal_worth:,.2f}</b>
        </div>
        """, unsafe_allow_html=True)