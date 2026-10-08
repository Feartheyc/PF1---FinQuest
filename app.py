import streamlit as st
from sidebar import render_sidebar
from utils import (
    img_to_base64, 
    render_interactive_dialogue, 
    render_language_selector, 
    t
)
from engine import init_game, try_apply_effects
from content import get_event_data, get_total_levels
from config import apply_custom_css
from leaderboard import render_leaderboard_ui
from phishing_game import render_phishing_game
from investmentsim import render_investmentsim

# ==========================================
# 1. APP CONFIGURATION & STATE INITIALIZATION
# ==========================================
st.set_page_config(page_title="Financial Journey", layout="wide", page_icon="🌏", initial_sidebar_state="collapsed")

if "selected_lang" not in st.session_state:
    st.session_state.selected_lang = "English"

if "game" not in st.session_state: 
    st.session_state.game = {"state": "MAIN_MENU"}

apply_custom_css()

# ==========================================
# 2. MENU RENDERING FUNCTIONS
# ==========================================
def render_main_menu():
    st.markdown(f"""
        <div class="menu-header-box">
            <div class="menu-title">🌏 {t("FinLife")}</div>
            <div class="menu-subtitle">{t("A Financial Literacy RPG Journey")}</div>
        </div>
    """, unsafe_allow_html=True)

    _, col_center, _ = st.columns([1, 2.2, 1])
    with col_center:
        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button(f"🚀 {t('START JOURNEY')}", use_container_width=True):
                st.session_state.game['state'] = "INTRO"
                st.rerun()
        with b_c2:
            if st.button(f"📜 {t('HOW TO PLAY')}", use_container_width=True):
                st.session_state.game['state'] = "TUTORIAL"
                st.rerun()

        b_c3, b_c4 = st.columns(2)
        with b_c3:
            if st.button(f"🛡️ {t('CYBER SHIELD')}", use_container_width=True):
                st.session_state.game['state'] = "CYBER_GAME"
                st.rerun()
        with b_c4:
            if st.button(f"❤️ {t('CREDITS')}", use_container_width=True):
                st.session_state.game['state'] = "CREDITS"
                st.rerun()

def render_credits():
    st.markdown(f'<div class="menu-title" style="font-size: 2.5rem; text-align:center;">{t("CREDITS")}</div>', unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div class="menu-card">
                <h3 style="color:#4ade80; margin-top:0;">{t("Developed By Team FinLife")}</h3>
                <p style="color:#94a3b8; font-size:0.85rem;">{t("Created for the Athrava Project Friday 2026")}</p>
                <hr style="border-color: #334155; margin: 15px 0;">
                <p style="text-align:left; font-size:0.9rem; line-height:1.6;">
                <b>• {t("Team")}:</b> Yuvraj Chavan, Akash Rana, Rishi Bhuta, Sufiyan Mukadam<br>
                <b>• {t("Tech Stack")}:</b> Python, Streamlit, Pandas, SQLite<br>
                <b>• {t("Features")}:</b> {t("RPG Gameplay, Stock Simulator, Cyber Safety")}<br>
                <b>• {t("Mission")}:</b> {t("Making financial literacy accessible to rural India.")}
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        if st.button(f"⬅ {t('BACK TO MENU')}", use_container_width=True):
            st.session_state.game['state'] = "MAIN_MENU"
            st.rerun()

def render_tutorial():
    st.markdown(f'<div class="menu-title" style="font-size: 2.5rem; text-align:center;">{t("HOW TO PLAY")}</div>', unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div class="menu-card" style="text-align: left;">
                <h4 style="color:#facc15; margin:0 0 5px 0;">1. {t("Choose Your Persona")}</h4>
                <p style="font-size:0.85rem; color:#cbd5e1; margin-bottom:12px;">{t("Select from Farmer, Student, Employee, or Founder. Each starts with distinct challenges.")}</p>
                <h4 style="color:#facc15; margin:0 0 5px 0;">2. {t("Evaluate Hidden Risks")}</h4>
                <p style="font-size:0.85rem; color:#cbd5e1; margin-bottom:12px;">{t("Options only show direct cash flow. Hidden debts, interest traps, and prudence points update silently based on your choices.")}</p>
                <h4 style="color:#facc15; margin:0 0 5px 0;">3. {t("Dynamic Investable Capital")}</h4>
                <p style="font-size:0.85rem; color:#cbd5e1; margin-bottom:12px;">{t("Your Investable Pool expands with high prudence and savings, but shrinks under heavy stress.")}</p>
                <h4 style="color:#facc15; margin:0 0 5px 0;">4. {t("Avoid Debt & Burnout")}</h4>
                <p style="font-size:0.85rem; color:#cbd5e1; margin:0;">{t("If your Stress reaches 100%, you enter emergency restructuring. Keep liabilities low!")}</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        if st.button(f"⬅ {t('BACK TO MENU')}", use_container_width=True):
            st.session_state.game['state'] = "MAIN_MENU"
            st.rerun()

# ==========================================
# 3. HELPERS
# ==========================================
def format_effects(effects):
    if "cash" in effects and effects["cash"] != 0:
        val = effects["cash"]
        sign = "+" if val > 0 else "-"
        return f" ({sign}₹{abs(val):,})"
    return ""

def render_hud_content(p):
    ins_status = f"✅ {t('Active')}" if p.get('insurance') else f"❌ {t('None')}"
    return f"""
    <div class="hud-container">
        <div class="hud-item"><div class="hud-label">{t("ROLE")}</div><div class="hud-value">{t(p['persona'])}</div></div>
        <div class="hud-item"><div class="hud-label">{t("CASH")}</div><div class="hud-value money-val">₹{p['cash']:,}</div></div>
        <div class="hud-item"><div class="hud-label">{t("SAVINGS")}</div><div class="hud-value money-val">₹{p['savings']:,}</div></div>
        <div class="hud-item"><div class="hud-label">{t("DEBT")}</div><div class="hud-value debt-val">₹{p['loan']:,}</div></div>
        <div class="hud-item"><div class="hud-label">{t("INVEST POOL")}</div><div class="hud-value invest-val">₹{p.get('investments', 0):,}</div></div>
        <div class="hud-item"><div class="hud-label">{t("SCORE")}</div><div class="hud-value" style="color:#67e8f9;">{p.get('score_points', 0)} pts</div></div>
        <div class="hud-item"><div class="hud-label">{t("STRESS")}</div><div class="hud-value stress-val">{p['stress']}%</div></div>
        <div class="hud-item"><div class="hud-label">{t("INSURANCE")}</div><div class="hud-value ins-val">{ins_status}</div></div>
    </div>
    """

def render_mini_map(persona, current_lvl):
    total_levels = get_total_levels(persona)

    dots_html = ""
    for i in range(total_levels):
        if i < current_lvl:
            status = "completed"
            content = "✓"
        elif i == current_lvl:
            status = "active"
            content = ""
        else:
            status = "pending"
            content = ""

        dots_html += f"<div class='step {status}'>{content}</div>"

        if i < total_levels - 1:
            line_status = "line-active" if i < current_lvl else "line-pending"
            dots_html += f"<div class='step-line {line_status}'></div>"

    return f"""
<style>
    .progress-wrapper {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 14px 24px;
        margin-bottom: 20px;
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }}
    .step {{
        width: 26px; height: 26px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 12px;
        z-index: 2;
        transition: all 0.3s;
    }}
    .step.completed {{ background: #4ade80; color: #064e3b; box-shadow: 0 0 8px rgba(74, 222, 128, 0.4); }}
    .step.active {{ 
        background: #ff5252; border: 2px solid white; 
        box-shadow: 0 0 12px rgba(255, 82, 82, 0.8); 
        transform: scale(1.25);
    }}
    .step.pending {{ background: #334155; border: 2px solid #475569; }}

    .step-line {{
        flex-grow: 1;
        height: 4px;
        margin: 0 4px;
        border-radius: 2px;
    }}
    .line-active {{ background: #4ade80; }}
    .line-pending {{ background: #334155; }}
</style>
<div class="progress-wrapper">
    {dots_html}
</div>
"""

# ==========================================
# 4. SCENE RENDERING
# ==========================================
def render_persona_selection():
    st.markdown(f"<h2 style='text-align:center;'>🌏 {t('Select Your Persona')}</h2>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    chars = [
        {"col": c1, "role": "Farmer", "img": "https://cdn-icons-png.flaticon.com/512/4825/4825021.png", "desc": "Crops, weather risks, seasonal loans.", "btn": "🚜 Select Farmer"},
        {"col": c2, "role": "Employee", "img": "https://cdn-icons-png.flaticon.com/512/4825/4825038.png", "desc": "Fixed salary, lifestyle debt, tax planning.", "btn": "👔 Select Employee"},
        {"col": c3, "role": "Student", "img": "https://cdn-icons-png.flaticon.com/512/4825/4825108.png", "desc": "Pocket money, exams, career investments.", "btn": "🎓 Select Student"},
        {"col": c4, "role": "Founder", "img": "https://cdn-icons-png.flaticon.com/512/4825/4825072.png", "desc": "Equity allocation, runway, scaling risk.", "btn": "🚀 Select Founder"}
    ]
    for char in chars:
        with char["col"]:
            st.markdown(f'<div class="char-card"><img src="{char["img"]}" class="char-img"><h4>{t(char["role"])}</h4><p style="font-size:0.8rem; color:#94a3b8;">{char["desc"]}</p></div>', unsafe_allow_html=True)
            if st.button(char["btn"], key=f"sel_{char['role']}", use_container_width=True):
                st.session_state.game = init_game(char["role"])
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(f"⬅ {t('Back to Main Menu')}", use_container_width=True):
        st.session_state.game['state'] = "MAIN_MENU"
        st.rerun()

def render_map():
    p = st.session_state.game
    current_lvl = p['event_index']
    st.markdown(render_hud_content(p), unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c1:
        persona_map_files = {"Farmer": "assets/map_farmer.png", "Student": "assets/map_student.png", "Employee": "assets/map_business.png", "Founder": "assets/map_startup.png"}
        target_map_file = persona_map_files.get(p['persona'], "assets/level_map.png")
        current_map_img = img_to_base64(target_map_file) or img_to_base64("assets/level_map.png")

        path = [(10, 80), (20, 70), (30, 75), (40, 60), (50, 50), (60, 45), (70, 55), (80, 40), (90, 30)]
        svg = f'<polyline points="{" ".join([f"{x*8},{y*6}" for x,y in path])}" fill="none" stroke="#ffd966" stroke-width="6" stroke-dasharray="10,5"/>'
        for idx, (bx, by) in enumerate(path):
            color = "#4ade80" if idx < current_lvl else ("#ff5252" if idx == current_lvl else "#64748b")
            svg += f'<circle cx="{bx*8}" cy="{by*6}" r="{15 if idx==current_lvl else 10}" fill="{color}" stroke="white" stroke-width="2"><animate attributeName="r" values="15;18;15" dur="1.5s" repeatCount="indefinite" /></circle>' if idx == current_lvl else f'<circle cx="{bx*8}" cy="{by*6}" r="10" fill="{color}" stroke="white" stroke-width="2"></circle>'

        st.html(f"""
        <style>
            #map-container {{ 
                width: 100%; 
                height: 550px; 
                background-image: url('data:image/png;base64,{current_map_img}'); 
                background-size: cover; 
                background-position: center; 
                border-radius: 12px; 
            }} 
        </style>
        <div id='map-container'>
            <svg viewBox='0 0 800 600' preserveAspectRatio='none'>{svg}</svg>
        </div>
        """)

    with c2:
        st.markdown(f"### {t('Level')} {current_lvl + 1}")
        evt = get_event_data(p['persona'], current_lvl)
        if evt:
            if st.button(f"🚀 {t('Enter Level')}", type="primary", use_container_width=True): 
                st.session_state.game['state'] = "PLAYING"
                st.rerun()
        else:
            if st.button(f"🏆 {t('Finish')}", type="primary"): 
                st.session_state.game['state'] = "END"
                st.rerun()

        st.markdown("---")
        st.markdown(f"### 🏛️ {t('NSE Terminal')}")
        if st.button(f"📈 {t('Open Stock Market')}", use_container_width=True):
            st.session_state.cash = float(p.get('investments', 1000))
            st.session_state.username = p['persona']
            st.session_state.game['state'] = "MARKET"
            st.rerun()

        st.markdown("---")
        if st.button(f"⬅ {t('Change Role')}"): 
            st.session_state.game['state'] = "INTRO"
            st.rerun()

def render_scene():
    p = st.session_state.game

    if p.get('stress', 0) >= 100:
        render_distress_screen(p)
        return

    evt = get_event_data(p['persona'], p['event_index'])
    if not evt: 
        p['state'] = "MAP"
        st.rerun()
        return

    render_sidebar(p)

    st.markdown(render_hud_content(p), unsafe_allow_html=True)
    st.markdown(render_mini_map(p['persona'], p['event_index']), unsafe_allow_html=True)
    st.markdown('<div class="scene-card">', unsafe_allow_html=True)

    if p.get('last_feedback'):
        st.markdown(f"<div class='game-alert alert-{p['feedback_type']}'>{t(p['last_feedback'])}</div>", unsafe_allow_html=True)
        p['last_feedback'] = None

    render_interactive_dialogue(evt["avatar"], evt["npc"], evt["story"])

    if "thought" in evt: 
        st.markdown(f'<div class="thought-container"><div class="thought-bubble">💭 <b>{t("Inner Thought")}:</b> {t(evt["thought"])}</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    if "advisor" in evt:
        with st.expander(f"💡 {t('Financial Principle & Trade-off')}"):
            st.markdown(f"**{t('Advisor Framework')}:**\n\n{t(evt['advisor'])}")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    if "choices" in evt:
        cols = st.columns(len(evt["choices"]))
        for i, (txt, eff) in enumerate(evt["choices"].items()):
            with cols[i]:
                btn_label = f"{t(txt)}{format_effects(eff)}"
                if st.button(btn_label, key=f"btn_{p['event_index']}_{i}", use_container_width=True):
                    msg = eff.pop('__msg', None)
                    success, s_msg = try_apply_effects(eff)
                    p['last_feedback'], p['feedback_type'] = (msg or s_msg), ("good" if success else "bad")
                    if success: 
                        p['event_index'] += 1
                    st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1, 4])
    with col_l:
        if st.button(f"🗺️ {t('Map')}", use_container_width=True): 
            p['state'] = "MAP"
            st.rerun()

def render_distress_screen(p):
    st.markdown("""
        <div class="scene-card" style="border: 2px solid #ef4444; background: rgba(69, 10, 10, 0.85); text-align: center;">
            <h1 style="color: #f87171;">⚠️ FINANCIAL BURNOUT & CRISIS</h1>
            <p style="font-size: 1.1rem; color: #fecaca;">
                Your Stress has reached 100%! Overwhelming debt service obligations and acute financial pressure have triggered an emergency intervention.
            </p>
            <p style="font-size: 0.95rem; color: #cbd5e1;">
                A financial counselor steps in to restructure your liabilities. Emergency liquidations and debt settlements will cut your stress, but at a severe penalty to your balance sheet.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚨 Restructure Debt & Liquidate Reserves", use_container_width=True, type="primary"):
            penalty = int(p['loan'] * 0.25)
            p['cash'] = max(0, p['cash'] - penalty)
            p['savings'] = max(0, p['savings'] - penalty)
            p['loan'] = max(0, p['loan'] - penalty)
            p['stress'] = 45
            p['score_points'] = max(0, p.get('score_points', 0) - 40)
            p['last_feedback'] = "Emergency Restructuring executed: Creditors accepted haircuts; non-core cash surrendered."
            p['feedback_type'] = "bad"
            st.rerun()

# ==========================================
# 5. MAIN APP LOOP
# ==========================================
render_language_selector()

state = st.session_state.game['state']

if state == "MAIN_MENU":
    render_main_menu()
elif state == "CREDITS":
    render_credits()
elif state == "TUTORIAL":
    render_tutorial()
elif state == "INTRO": 
    render_persona_selection()
elif state == "CYBER_GAME": 
    render_phishing_game()
elif state == "MAP": 
    render_map()
elif state == "PLAYING": 
    render_scene()
elif state == "MARKET":
    render_investmentsim()
elif state == "END":
    p = st.session_state.game
    nw = (p['cash'] + p['savings'] + p.get('investments', 0)) - p['loan']
    st.balloons()
    st.markdown(f"<div class='menu-card'><h1>{t('Journey Complete')}</h1><h2>{t('Net Worth')}: ₹{nw:,}</h2><p style='color:#67e8f9;'>Final Literacy Score: {p.get('score_points', 0)} pts</p></div>", unsafe_allow_html=True)
    render_leaderboard_ui(final_score=nw)
    if st.button(f"↺ {t('Restart Journey')}", use_container_width=True): 
        st.session_state.game = {"state": "MAIN_MENU"}
        st.rerun()