import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

        /* --- GLOBAL APP THEME --- */
        .stApp { 
            background: radial-gradient(circle at top, #1e1b4b 0%, #020617 100%); 
            color: #e2e8f0; 
            font-family: 'Poppins', sans-serif; 
        }

        /* Hard kill all Streamlit spinners & status hooks */
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
            height: 2.2rem !important;
        }

        /* Generous, clean width for gameplay */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-width: 1050px !important;
        }

        @keyframes slideUp { 
            from { opacity: 0; transform: translateY(15px); } 
            to { opacity: 1; transform: translateY(0); } 
        }

        /* --- HERO HEADER (MAIN MENU) --- */
        .menu-header-box {
            text-align: center;
            margin-top: 0.5rem;
            margin-bottom: 1.2rem;
        }

        .menu-title {
            text-align: center;
            font-size: 3.2rem;
            font-weight: 800;
            line-height: 1.1;
            margin: 0;
            background: linear-gradient(to bottom, #4ade80, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(74, 222, 128, 0.25);
            letter-spacing: -1px;
        }

        .menu-subtitle {
            text-align: center;
            color: #94a3b8;
            font-size: 0.85rem;
            letter-spacing: 3px;
            margin-top: 6px;
            text-transform: uppercase;
        }

        /* --- BUTTONS --- */
        .stButton > button {
            width: 100%;
            background: rgba(30, 41, 59, 0.75) !important;
            border: 1px solid #334155 !important;
            padding: 14px 18px !important;
            border-radius: 12px !important;
            color: #f1f5f9 !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            font-size: 0.88rem !important;
            line-height: 1.3 !important;
            white-space: normal !important;
            word-wrap: break-word !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            text-align: center !important;
        }

        .stButton > button:hover {
            border-color: #4ade80 !important;
            color: #4ade80 !important;
            background: rgba(74, 222, 128, 0.15) !important;
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.4), 0 0 12px rgba(74, 222, 128, 0.2);
        }

        /* --- ROOMY HUD BAR (ALL IN 1 ROW) --- */
        .hud-container { 
            background: rgba(15, 23, 42, 0.85); 
            backdrop-filter: blur(12px); 
            border: 1px solid rgba(255, 255, 255, 0.1); 
            border-radius: 16px; 
            padding: 12px 16px; 
            display: flex; 
            flex-direction: row;
            justify-content: space-between; 
            align-items: center;
            gap: 10px; 
            margin-bottom: 20px; 
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); 
        }

        .hud-item { 
            text-align: center; 
            flex: 1 1 0;
            min-width: 0;
            padding: 8px 6px; 
            background: rgba(255, 255, 255, 0.03); 
            border-radius: 10px; 
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .hud-label { 
            font-size: 0.65rem; 
            color: #94a3b8; 
            text-transform: uppercase; 
            letter-spacing: 0.8px;
            margin-bottom: 4px; 
            font-weight: 600;
        }
        .hud-value { 
            font-family: 'Space Mono', monospace; 
            font-size: 0.92rem; 
            font-weight: 700; 
            color: #f8fafc; 
            white-space: nowrap;
        }
        .money-val { color: #4ade80; } 
        .debt-val { color: #f87171; } 
        .stress-val { color: #facc15; }
        .invest-val { color: #c084fc; }
        .ins-val { color: #38bdf8; }

        /* --- SCENE CARD & INTERACTIVE AREA --- */
        .scene-card { 
            background: linear-gradient(145deg, #1e293b, #0f172a); 
            border: 1px solid #334155; 
            border-radius: 20px; 
            padding: 24px 28px; 
            margin-bottom: 20px; 
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5); 
            animation: slideUp 0.4s ease-out; 
            position: relative; 
        }
        .scene-card::before { 
            content: ""; 
            position: absolute; 
            top: 0; left: 0; 
            width: 100%; height: 4px; 
            background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899); 
            border-radius: 20px 20px 0 0;
        }

        .thought-container { 
            display: flex; 
            justify-content: flex-start; 
            margin-top: 16px; 
            margin-bottom: 8px; 
        }
        .thought-bubble { 
            background: rgba(99, 102, 241, 0.12); 
            border: 1px dashed #6366f1; 
            color: #c7d2fe; 
            padding: 12px 18px; 
            border-radius: 14px; 
            font-style: italic; 
            font-size: 0.92rem; 
            width: 100%;
            line-height: 1.5;
        }

        .game-alert { 
            padding: 14px; 
            border-radius: 10px; 
            margin-bottom: 16px; 
            text-align: center; 
            font-weight: 600; 
            font-size: 0.95rem;
        }
        .alert-good { background: rgba(6, 78, 59, 0.85); border: 1px solid #059669; color: #6ee7b7; }
        .alert-bad { background: rgba(127, 29, 29, 0.85); border: 1px solid #dc2626; color: #fca5a5; }
        .alert-info { background: rgba(30, 58, 138, 0.85); border: 1px solid #2563eb; color: #bfdbfe; }

        .menu-card {
            background: rgba(15, 23, 42, 0.85);
            border: 1px solid #334155;
            padding: 24px;
            border-radius: 16px;
            text-align: center;
            backdrop-filter: blur(10px);
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5);
        }

        .char-card { background-color: #1e293b; border: 2px solid #334155; border-radius: 12px; padding: 15px; text-align: center; transition: 0.25s; height: 100%; }
        .char-card:hover { transform: translateY(-4px); border-color: #38bdf8; }
        .char-img { width: 85px; height: 85px; border-radius: 50%; margin-bottom: 10px; object-fit: cover; border: 2px solid #475569; }

        #map-container { border: 2px solid #334155; box-shadow: 0 0 20px rgba(0,0,0,0.5); }

        div[data-testid="stDialog"] {
            background-color: #1e293b;
            color: #e2e8f0;
            border: 1px solid #334155;
        }
    </style>
    """, unsafe_allow_html=True)