import streamlit as st
import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime

DB_FILE = "portfolio.db"

def get_connection():
    return sqlite3.connect(DB_FILE, timeout=10, check_same_thread=False)

def init_sim_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            cash REAL
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            stock TEXT,
            qty INTEGER,
            price REAL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
        """)
        conn.commit()

TICKERS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "HINDUNILVR.NS",
    "ICICIBANK.NS", "KOTAKBANK.NS", "LT.NS", "SBIN.NS", "AXISBANK.NS",
    "BAJFINANCE.NS", "BHARTIARTL.NS", "MARUTI.NS", "ITC.NS", "ASIANPAINT.NS",
    "HCLTECH.NS", "ULTRACEMCO.NS", "NESTLEIND.NS", "POWERGRID.NS", "ONGC.NS",
    "TITAN.NS", "ADANIPORTS.NS", "GRASIM.NS", "WIPRO.NS", "JSWSTEEL.NS",
    "SUNPHARMA.NS", "DRREDDY.NS", "HDFCLIFE.NS", "DIVISLAB.NS", "TECHM.NS",
    "COALINDIA.NS", "TATASTEEL.NS", "M&M.NS", "BPCL.NS", "BRITANNIA.NS",
    "IOC.NS", "CIPLA.NS", "SHREECEM.NS", "INDUSINDBK.NS", "EICHERMOT.NS"
]

@st.cache_data(ttl=600)
def fetch_stocks(tickers):
    try:
        df = yf.download(tickers, period="1mo", interval="1d", group_by="ticker", progress=False)
        closes = {}
        for t in tickers:
            if t in df and "Close" in df[t]:
                s = df[t]["Close"].dropna()
                if not s.empty:
                    closes[t] = s
        return pd.DataFrame(closes)
    except Exception as e:
        st.warning(f"Error loading market data: {e}")
        return pd.DataFrame()

def render_investmentsim():
    init_sim_db()

    if "cash" not in st.session_state:
        st.session_state.cash = 10000.0
    if "transactions" not in st.session_state:
        st.session_state.transactions = []
    if "username" not in st.session_state:
        st.session_state.username = None

    # Load active persona cash if logged in via game
    if "game" in st.session_state and not st.session_state.username:
        st.session_state.username = st.session_state.game.get("persona", "Player")
        st.session_state.cash = float(st.session_state.game.get("cash", 10000))

    prices = fetch_stocks(TICKERS)
    if prices.empty:
        st.error("Market data currently unavailable. Please check internet connection.")
        if st.button("⬅ Return to Game Map"):
            st.session_state.game['state'] = "MAP"
            st.rerun()
        return

    latest_prices = prices.iloc[-1]

    # --- SIDEBAR CONTROLS ---
    st.sidebar.header("🏛️ NSE Terminal")
    st.sidebar.write(f"Account: **{st.session_state.username}**")

    st.sidebar.subheader("Trade Equities")
    stock_choice = st.sidebar.selectbox("Select Stock", list(latest_prices.index), key="stock_choice")
    current_price = float(latest_prices[stock_choice])
    st.sidebar.write(f"Current Price: ₹{current_price:,.2f}")
    
    action = st.sidebar.radio("Action", ["Buy", "Sell"], key="action_choice")
    quantity = st.sidebar.number_input("Quantity", min_value=1, value=1, step=1, key="qty_input")

    if st.sidebar.button("Execute Trade", key="execute_trade"):
        with get_connection() as conn:
            c = conn.cursor()
            trade_cost = current_price * quantity

            if action == "Buy":
                if trade_cost <= st.session_state.cash:
                    st.session_state.cash -= trade_cost
                    tx = {"date": str(prices.index[-1]), "stock": stock_choice, "qty": quantity, "price": current_price}
                    st.session_state.transactions.append(tx)
                    c.execute("INSERT INTO transactions(username, date, stock, qty, price) VALUES (?, ?, ?, ?, ?)",
                              (st.session_state.username, tx["date"], tx["stock"], tx["qty"], tx["price"]))
                    c.execute("INSERT OR REPLACE INTO users(username, cash) VALUES (?, ?)", (st.session_state.username, st.session_state.cash))
                    conn.commit()
                    st.sidebar.success(f"Bought {quantity} shares of {stock_choice}")
                else:
                    st.sidebar.error("Insufficient Cash balance!")

            elif action == "Sell":
                total_held = sum(t["qty"] for t in st.session_state.transactions if t["stock"] == stock_choice)
                if total_held >= quantity:
                    st.session_state.cash += trade_cost
                    tx = {"date": str(prices.index[-1]), "stock": stock_choice, "qty": -quantity, "price": current_price}
                    st.session_state.transactions.append(tx)
                    c.execute("INSERT INTO transactions(username, date, stock, qty, price) VALUES (?, ?, ?, ?, ?)",
                              (st.session_state.username, tx["date"], tx["stock"], tx["qty"], tx["price"]))
                    c.execute("INSERT OR REPLACE INTO users(username, cash) VALUES (?, ?)", (st.session_state.username, st.session_state.cash))
                    conn.commit()
                    st.sidebar.success(f"Sold {quantity} shares of {stock_choice}")
                else:
                    st.sidebar.error("Not enough shares to sell!")

    # --- PORTFOLIO DASHBOARD ---
    st.header("💼 Live Portfolio Summary")
    st.metric("Liquid Cash", f"₹{st.session_state.cash:,.2f}")

    portfolio = {}
    for t in st.session_state.transactions:
        portfolio[t["stock"]] = portfolio.get(t["stock"], 0) + t["qty"]
    portfolio = {k: v for k, v in portfolio.items() if v > 0}

    total_stock_value = 0.0
    if portfolio:
        portfolio_rows = []
        for s, q in portfolio.items():
            s_price = float(latest_prices.get(s, 0.0))
            s_val = s_price * q
            total_stock_value += s_val
            portfolio_rows.append({"Stock": s, "Quantity": q, "Market Price": round(s_price, 2), "Total Value": round(s_val, 2)})

        st.dataframe(pd.DataFrame(portfolio_rows), use_container_width=True)
        st.metric("Equities Value", f"₹{total_stock_value:,.2f}")
    else:
        st.info("No active holdings.")

    st.markdown("---")
    if st.button("🗺️ Return to Game Map", use_container_width=True, key="return_map_btn"):
        if "game" in st.session_state:
            st.session_state.game['cash'] = int(st.session_state.cash)
            st.session_state.game['investments'] = int(total_stock_value)
            st.session_state.game['state'] = "MAP"
        st.rerun()