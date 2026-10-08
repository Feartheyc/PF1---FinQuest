import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

        /* --- GLOBAL APP THEME --- */
        .stApp { 
            background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #080c1b 70%, #020617 100%); 
            color: #e2e8f0; 
            font-family: 'Poppins', sans-serif; 
        }

        /* Suppress Streamlit default status & spinners */
        div[data-testid="stStatusWidget"],
        .stSpinner,
        div[class*="stSpinner"],
        div[data-testid="stNotification"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        div[data-stale="true"] {
            opacity: 1 !important;
            filter: none !important;
        }

        header[data-testid="stHeader"] {
            background: transparent !important;
            height: 2rem !important;
        }

        /* Generous canvas width with breathing room */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 3rem !important;
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            max-width: 1080px !important;
        }

        /* --- ROOMY HUD BAR --- */
        .hud-container { 
            background: rgba(15, 23, 42, 0.75); 
            backdrop-filter: blur(16px); 
            border: 1px solid rgba(255, 255, 255, 0.08); 
            border-radius: 18px; 
            padding: 14px 20px; 
            display: flex; 
            flex-direction: row;
            justify-content: space-between; 
            align-items: center;
            gap: 12px; 
            margin-bottom: 24px; 
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5); 
        }

        .hud-item { 
            text-align: center; 
            flex: 1 1 0;
            min-width: 0;
            padding: 10px 8px; 
            background: rgba(255, 255, 255, 0.02); 
            border-radius: 12px; 
            border: 1px solid rgba(255, 255, 255, 0.04);
            transition: all 0.2s ease;
        }
        .hud-item:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(255, 255, 255, 0.08);
        }
        .hud-label { 
            font-size: 0.68rem; 
            color: #94a3b8; 
            text-transform: uppercase; 
            letter-spacing: 1px;
            margin-bottom: 5px; 
            font-weight: 600;
        }
        .hud-value { 
            font-family: 'Space Mono', monospace; 
            font-size: 0.95rem; 
            font-weight: 700; 
            color: #f8fafc; 
            white-space: nowrap;
        }
        .money-val { color: #4ade80; } 
        .debt-val { color: #f87171; } 
        .stress-val { color: #facc15; }
        .invest-val { color: #c084fc; }
        .ins-val { color: #38bdf8; }

        /* --- UNIFIED SCENE PRESENTATION CARD --- */
        .scene-card { 
            background: linear-gradient(160deg, rgba(30, 41, 59, 0.65) 0%, rgba(15, 23, 42, 0.85) 100%); 
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08); 
            border-radius: 20px; 
            padding: 24px 28px; 
            margin-bottom: 24px; 
            box-shadow: 0 16px 36px -12px rgba(0, 0, 0, 0.6); 
            position: relative; 
        }

        .thought-bubble { 
            background: rgba(99, 102, 241, 0.08); 
            border: 1px solid rgba(129, 140, 248, 0.25); 
            color: #c7d2fe; 
            padding: 14px 20px; 
            border-radius: 14px; 
            font-size: 0.93rem; 
            line-height: 1.6;
            margin-top: 18px;
        }

        /* --- ADVISOR EXPANDER --- */
        div[data-testid="stExpander"] {
            border: 1px solid rgba(250, 204, 21, 0.2) !important;
            border-radius: 14px !important;
            background: rgba(15, 23, 42, 0.4) !important;
            margin-bottom: 24px !important;
        }
        div[data-testid="stExpander"] summary {
            padding: 12px 18px !important;
            color: #facc15 !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
        }

        /* --- DECISION ACTION BUTTONS --- */
        .stButton > button {
            width: 100%;
            background: linear-gradient(145deg, #1e293b, #0f172a) !important;
            border: 1px solid #334155 !important;
            padding: 18px 24px !important;
            border-radius: 14px !important;
            color: #f8fafc !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            font-size: 0.92rem !important;
            line-height: 1.4 !important;
            white-space: normal !important;
            word-wrap: break-word !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            text-align: center !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        }

        .stButton > button:hover {
            border-color: #38bdf8 !important;
            color: #38bdf8 !important;
            background: linear-gradient(145deg, #1e293b, #1e2238) !important;
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5), 0 0 15px rgba(56, 189, 248, 0.2) !important;
        }

        /* Primary action styling */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
            border-color: #3b82f6 !important;
        }

        /* Alerts */
        .game-alert { 
            padding: 14px 20px; 
            border-radius: 12px; 
            margin-bottom: 20px; 
            text-align: center; 
            font-weight: 600; 
            font-size: 0.95rem;
        }
        .alert-good { background: rgba(6, 78, 59, 0.8); border: 1px solid #059669; color: #6ee7b7; }
        .alert-bad { background: rgba(127, 29, 29, 0.8); border: 1px solid #dc2626; color: #fca5a5; }
        .alert-info { background: rgba(30, 58, 138, 0.8); border: 1px solid #2563eb; color: #bfdbfe; }

        /* Menu Elements */
        .menu-header-box { text-align: center; margin-top: 1rem; margin-bottom: 2rem; }
        .menu-title {
            font-size: 3.5rem; font-weight: 800; line-height: 1.1; margin: 0;
            background: linear-gradient(to bottom, #4ade80, #3b82f6);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-shadow: 0 0 25px rgba(74, 222, 128, 0.2);
        }
        .menu-subtitle { color: #94a3b8; font-size: 0.9rem; letter-spacing: 3px; margin-top: 8px; text-transform: uppercase; }
        .menu-card {
            background: rgba(15, 23, 42, 0.85); border: 1px solid #334155; padding: 28px;
            border-radius: 18px; text-align: center; box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5);
        }
        .char-card { background-color: #1e293b; border: 2px solid #334155; border-radius: 14px; padding: 18px; text-align: center; transition: 0.25s; }
        .char-card:hover { transform: translateY(-4px); border-color: #38bdf8; }
        .char-img { width: 85px; height: 85px; border-radius: 50%; margin-bottom: 12px; object-fit: cover; border: 2px solid #475569; }
    </style>
    """, unsafe_allow_html=True)